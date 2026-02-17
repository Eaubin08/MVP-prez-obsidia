
#!/usr/bin/env python3
import os, subprocess, sys

def detect_repo():
    if os.path.exists("obsidia_os1") or os.path.exists("contract.py"):
        return "obsidia"
    if os.path.exists("src") or os.path.exists("gates"):
        return "trading"
    return "unknown"

repo = detect_repo()
if repo == "unknown":
    print("Repo type not detected.")
    sys.exit(1)

print(f"Detected repo: {repo}")
cmd = ["pytest", "-q"]
res = subprocess.run(cmd)
sys.exit(res.returncode)
