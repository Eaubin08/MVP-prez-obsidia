import os
import re

def _scan_py_files(folder: str):
    for root, _, files in os.walk(folder):
        for fn in files:
            if fn.endswith(".py"):
                path = os.path.join(root, fn)
                with open(path, "r", encoding="utf-8") as f:
                    yield path, f.read()

def test_os0_never_imports_os1_or_os2():
    root = os.path.dirname(os.path.dirname(__file__))
    os0 = os.path.join(root, "src", "obsidia_os0")
    forbidden = ["obsidia_os1", "obsidia_os2"]
    for path, content in _scan_py_files(os0):
        for word in forbidden:
            assert word not in content, f"Forbidden import reference {word} in {path}"

def test_os2_never_imports_os0_or_os1():
    root = os.path.dirname(os.path.dirname(__file__))
    os2 = os.path.join(root, "src", "obsidia_os2")
    forbidden = ["obsidia_os0", "obsidia_os1"]
    for path, content in _scan_py_files(os2):
        for word in forbidden:
            assert word not in content, f"Forbidden import reference {word} in {path}"

def test_os1_may_import_os0_and_os2_only():
    root = os.path.dirname(os.path.dirname(__file__))
    os1 = os.path.join(root, "src", "obsidia_os1")
    forbidden = ["from forge_os", "import forge_os"]
    for path, content in _scan_py_files(os1):
        for word in forbidden:
            assert word not in content, f"Unexpected cross-package import {word} in {path}"
