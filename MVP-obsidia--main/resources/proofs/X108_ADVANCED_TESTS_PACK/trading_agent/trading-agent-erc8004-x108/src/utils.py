import json
from pathlib import Path
from datetime import datetime

def now_iso():
    return datetime.utcnow().isoformat() + "Z"

def append_jsonl(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
