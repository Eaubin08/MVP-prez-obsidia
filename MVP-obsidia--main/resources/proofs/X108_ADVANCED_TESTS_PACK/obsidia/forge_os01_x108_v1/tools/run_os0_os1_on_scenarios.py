#!/usr/bin/env python3
"""Runner OS0↔OS1 sur des scénarios JSON.

Entrée JSON = liste de scénarios comme produit par convert_x108_zips_to_json.py

Sortie:
- report.json (détaillé)
- report.csv (résumé)
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List

from obsidia_os1.os1 import run_request


def _load_json(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Scenario JSON must be a list")
    return data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenarios", required=True, help="Path to scenarios JSON")
    ap.add_argument("--outdir", default="out", help="Output directory")
    ap.add_argument("--contract", default=None, help="Optional contract JSON")
    args = ap.parse_args()

    scenarios_path = Path(args.scenarios).resolve()
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    scenarios = _load_json(scenarios_path)

    # optional contract (very small)
    contract_obj = None
    if args.contract:
        with Path(args.contract).open("r", encoding="utf-8") as f:
            contract_obj = json.load(f)

    results: List[Dict[str, Any]] = []
    for sc in scenarios:
        req = {
            "text": sc.get("text", "noop"),
            "x108": {
                "time_elapsed": float(sc.get("time_elapsed", 0.0)),
                "IST": float(sc.get("IST", 0.0)),
                "CMEC": float(sc.get("CMEC", 0.0)),
                "irreversible": bool(sc.get("irreversible", True)),
            },
            "contract": contract_obj,
        }
        dec = run_request(req)
        results.append(
            {
                "id": sc.get("id"),
                "decision": dec.decision,
                "contract_ok": dec.contract_ok,
                "x108_decision": dec.x108.decision,
                "wait_s": dec.x108.wait_s,
                "x108_reason": dec.x108.reason,
                "ssr": dec.ssr,
            }
        )

    report_json = outdir / "report.json"
    report_csv = outdir / "report.csv"

    with report_json.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    with report_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "decision",
                "contract_ok",
                "x108_decision",
                "wait_s",
                "x108_reason",
            ],
        )
        w.writeheader()
        for r in results:
            w.writerow({k: r.get(k) for k in w.fieldnames})

    # summary to stdout
    total = len(results)
    act = sum(1 for r in results if r["decision"] == "ACT")
    hold = sum(1 for r in results if r["decision"] == "HOLD")
    rej = sum(1 for r in results if r["decision"] == "REJECT")
    print(f"Total: {total} | ACT: {act} | HOLD: {hold} | REJECT: {rej}")
    print(f"Wrote: {report_csv}")


if __name__ == "__main__":
    main()
