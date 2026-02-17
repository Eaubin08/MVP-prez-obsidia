import json
import time
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional

def now_iso():
    return datetime.utcnow().isoformat() + "Z"

def append_jsonl(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def ensure_dirs(base_dir: Path) -> None:
    """Crée les répertoires nécessaires."""
    traces_dir = base_dir / "traces"
    traces_dir.mkdir(parents=True, exist_ok=True)
    (traces_dir / "last_run").mkdir(parents=True, exist_ok=True)

def log_jsonl(base_dir: Path, name: str, obj: Dict[str, Any]) -> None:
    """Ajoute une entrée dans un log JSONL."""
    ensure_dirs(base_dir)
    path = base_dir / "traces" / f"{name}.jsonl"
    obj = dict(obj)
    obj.setdefault("ts", time.time())
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def save_artifact(base_dir: Path, filename: str, data: Any) -> Path:
    """Sauvegarde un artifact JSON."""
    ensure_dirs(base_dir)
    out = base_dir / "traces" / "last_run" / filename
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return out

def read_artifact(base_dir: Path, filename: str) -> Optional[Dict[str, Any]]:
    """Lit un artifact JSON."""
    path = base_dir / "traces" / "last_run" / filename
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def zip_last_run(base_dir: Path) -> Path:
    """Crée un ZIP de tous les artifacts de last_run."""
    ensure_dirs(base_dir)
    zpath = base_dir / "traces" / "last_run" / "artifacts.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        last_run_dir = base_dir / "traces" / "last_run"
        for p in last_run_dir.glob("*"):
            if p.name.endswith(".zip"):
                continue
            z.write(p, arcname=p.name)
    return zpath
