# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all, collect_submodules
import sys

# add --test argument
if "--test" in sys.argv:
    print("OK")
    sys.exit(0)

packages = [
    "webview",
    "fastapi",
    "starlette",
    "uvicorn",
    "sqlalchemy",
    "apscheduler",
    "jinja2",
    "pydantic",
    "requests",
    "loguru",
    "dotenv",
    "cefpython3"
]

datas = [
    ("app", "app"),
    ("main.py", "."),
    ("static", "static"),
    (".env", "."),
]

binaries = []
hiddenimports = []

for pkg in packages:
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

hiddenimports += collect_submodules("app")

a = Analysis(
    ["UI.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "rich"],   # إن لم تستخدمه
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Appointments",
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name="Appointments",
)
