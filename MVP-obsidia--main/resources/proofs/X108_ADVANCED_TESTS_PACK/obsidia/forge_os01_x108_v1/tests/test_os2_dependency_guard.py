import os
import re

def test_os2_has_no_forbidden_imports():
    root = os.path.dirname(os.path.dirname(__file__))
    os2_path = os.path.join(root, "src", "obsidia_os2")
    forbidden = ["obsidia_os0", "obsidia_os1"]
    for fname in os.listdir(os2_path):
        if fname.endswith(".py"):
            with open(os.path.join(os2_path, fname), "r", encoding="utf-8") as f:
                content = f.read()
                for word in forbidden:
                    assert word not in content
