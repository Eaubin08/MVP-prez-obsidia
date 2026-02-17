#!/usr/bin/env python3
"""Convertisseur automatique X108 ZIP -> JSON scénarios.

Objectif:
- Prendre 1..N zips X108.
- Chercher des fichiers .csv/.csv.gz/.json déjà présents.
- Si rien trouvé: générer un dataset de scénarios minimal.

Sortie JSON:
[
  {"id":"...", "time_elapsed":..., "IST":..., "CMEC":..., "irreversible":true, "raw_source": ...},
  ...
]

Ce script est volontairement robuste/heuristique: il ne suppose pas un format unique.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import os
import random
import re
import zipfile
from typing import Any, Dict, Iterable, List, Optional, Tuple


def _iter_zip_members(z: zipfile.ZipFile) -> Iterable[zipfile.ZipInfo]:
    for info in z.infolist():
        if info.is_dir():
            continue
        yield info


def _read_text_from_zip(z: zipfile.ZipFile, name: str, limit_bytes: int = 10_000_000) -> str:
    with z.open(name) as f:
        b = f.read(limit_bytes)
    return b.decode("utf-8", errors="replace")


def _read_json_from_zip(z: zipfile.ZipFile, name: str) -> Any:
    txt = _read_text_from_zip(z, name)
    return json.loads(txt)


def _read_csv_rows_from_bytes(data: bytes, is_gz: bool) -> List[Dict[str, str]]:
    if is_gz:
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as gf:
            txt = gf.read().decode("utf-8", errors="replace")
    else:
        txt = data.decode("utf-8", errors="replace")

    # auto dialect
    sample = txt[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample)
    except Exception:
        dialect = csv.excel

    reader = csv.DictReader(io.StringIO(txt), dialect=dialect)
    rows: List[Dict[str, str]] = []
    for row in reader:
        if row is None:
            continue
        rows.append({k: (v if v is not None else "") for k, v in row.items()})
    return rows


def _normalize_row(row: Dict[str, str], idx: int, source: str) -> Dict[str, Any]:
    # mapping tolérant des champs attendus
    def f(key_candidates: List[str], default: float) -> float:
        for k in key_candidates:
            if k in row and str(row[k]).strip() != "":
                try:
                    return float(str(row[k]).strip())
                except Exception:
                    pass
        return default

    def b(key_candidates: List[str], default: bool) -> bool:
        for k in key_candidates:
            if k in row and str(row[k]).strip() != "":
                v = str(row[k]).strip().lower()
                if v in ("true", "1", "yes", "y", "oui"):
                    return True
                if v in ("false", "0", "no", "n", "non"):
                    return False
        return default

    time_elapsed = f(["time_elapsed", "t", "elapsed", "elapsed_s", "seconds"], 0.0)
    ist = f(["IST", "ist", "integrity", "score_ist"], 0.0)
    cmec = f(["CMEC", "cmec", "criticality", "score_cmec"], 0.0)
    irreversible = b(["irreversible", "irrev", "is_irreversible"], True)

    scenario_id = row.get("id") or row.get("scenario") or row.get("name") or f"{source}#{idx}"

    return {
        "id": str(scenario_id),
        "time_elapsed": float(time_elapsed),
        "IST": float(ist),
        "CMEC": float(cmec),
        "irreversible": bool(irreversible),
        "raw_source": source,
    }


def extract_scenarios_from_zip(zip_path: str, limit: int = 1000) -> List[Dict[str, Any]]:
    scenarios: List[Dict[str, Any]] = []

    with zipfile.ZipFile(zip_path, "r") as z:
        members = list(_iter_zip_members(z))

        # 1) JSON direct
        json_candidates = [m.filename for m in members if m.filename.lower().endswith(".json")]
        for name in json_candidates:
            try:
                obj = _read_json_from_zip(z, name)
                if isinstance(obj, list):
                    for i, item in enumerate(obj):
                        if isinstance(item, dict):
                            item2 = {
                                "id": str(item.get("id", f"{name}#{i}")),
                                "time_elapsed": float(item.get("time_elapsed", item.get("t", 0.0))),
                                "IST": float(item.get("IST", item.get("ist", 0.0))),
                                "CMEC": float(item.get("CMEC", item.get("cmec", 0.0))),
                                "irreversible": bool(item.get("irreversible", True)),
                                "raw_source": f"{os.path.basename(zip_path)}::{name}",
                            }
                            scenarios.append(item2)
                            if len(scenarios) >= limit:
                                return scenarios
                # if dict, ignore (too ambiguous)
            except Exception:
                continue

        # 2) CSV / CSV.GZ
        csv_candidates: List[Tuple[str, bool]] = []
        for m in members:
            fn = m.filename.lower()
            if fn.endswith(".csv"):
                csv_candidates.append((m.filename, False))
            elif fn.endswith(".csv.gz") or fn.endswith(".gz"):
                # only keep gz that likely contains csv
                if "csv" in fn:
                    csv_candidates.append((m.filename, True))

        for name, is_gz in csv_candidates:
            try:
                with z.open(name) as f:
                    data = f.read(20_000_000)
                rows = _read_csv_rows_from_bytes(data, is_gz=is_gz)
                for i, row in enumerate(rows[: max(0, limit - len(scenarios))]):
                    scenarios.append(_normalize_row(row, i, f"{os.path.basename(zip_path)}::{name}"))
                if len(scenarios) >= limit:
                    return scenarios
            except Exception:
                continue

        # 3) Heuristique: script python qui contient une liste/dict de scénarios
        py_candidates = [m.filename for m in members if m.filename.lower().endswith(".py")]
        for name in py_candidates:
            try:
                txt = _read_text_from_zip(z, name)
                # extraction naive des tuples (time_elapsed, IST, CMEC)
                triples = re.findall(r"\(\s*([0-9]+\.?[0-9]*)\s*,\s*([0-9]+\.?[0-9]*)\s*,\s*([0-9]+\.?[0-9]*)\s*\)", txt)
                for i, (t, ist, cmec) in enumerate(triples[: max(0, limit - len(scenarios))]):
                    scenarios.append(
                        {
                            "id": f"{os.path.basename(zip_path)}::{name}#{i}",
                            "time_elapsed": float(t),
                            "IST": float(ist),
                            "CMEC": float(cmec),
                            "irreversible": True,
                            "raw_source": f"{os.path.basename(zip_path)}::{name}",
                        }
                    )
                if len(scenarios) >= limit:
                    return scenarios
            except Exception:
                continue

    return scenarios


def generate_fallback_scenarios(n: int, seed: int = 108) -> List[Dict[str, Any]]:
    random.seed(seed)
    out = []
    for i in range(n):
        t = random.choice([0.0, 1.0, 10.0, 30.0, 60.0, 120.0, 300.0, 600.0])
        ist = random.uniform(0.0, 1.0)
        cmec = random.uniform(0.0, 1.0)
        irrev = random.choice([True, True, True, False])
        out.append({"id": f"fallback#{i}", "time_elapsed": t, "IST": ist, "CMEC": cmec, "irreversible": irrev, "raw_source": "fallback"})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zips", nargs="*", default=[], help="Paths to X108 zip packs")
    ap.add_argument("--limit", type=int, default=1000, help="Max scenarios per zip")
    ap.add_argument("--fallback", type=int, default=200, help="If nothing extracted, generate this many")
    ap.add_argument("--out", required=True, help="Output JSON file")
    args = ap.parse_args()

    scenarios: List[Dict[str, Any]] = []
    for zp in args.zips:
        if not os.path.exists(zp):
            continue
        scenarios.extend(extract_scenarios_from_zip(zp, limit=args.limit))

    if not scenarios:
        scenarios = generate_fallback_scenarios(args.fallback)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(scenarios)} scenarios to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
