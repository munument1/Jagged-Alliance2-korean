#!/usr/bin/env python3
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_TAUNTS = ROOT / "Patch" / "Data" / "TableData" / "EnemyTaunts"
V113_TAUNTS = ROOT / "Patch" / "Data-1.13" / "TableData" / "EnemyTaunts"
NPCDATA = ROOT / "Patch" / "Data" / "NPCData"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    civ_files = sorted(NPCDATA.glob("civ*.edt")) + sorted(NPCDATA.glob("CIV*.EDT"))
    if civ_files:
        fail("placeholder/loose CIV EDT files must not be shipped: " + ", ".join(p.name for p in civ_files))

    if not DATA_TAUNTS.is_dir() or not V113_TAUNTS.is_dir():
        fail("both Data and Data-1.13 EnemyTaunts directories must exist")

    data_files = {p.name: p for p in DATA_TAUNTS.glob("EnemyTaunts*.xml")}
    v113_files = {p.name: p for p in V113_TAUNTS.glob("EnemyTaunts*.xml")}

    if not data_files:
        fail("no EnemyTaunts XML files found")
    if set(data_files) != set(v113_files):
        missing_high = sorted(set(data_files) - set(v113_files))
        extra_high = sorted(set(v113_files) - set(data_files))
        fail(f"EnemyTaunts mirror mismatch; missing in Data-1.13={missing_high}, extra={extra_high}")

    warnings = []
    for name in sorted(data_files):
        low = data_files[name]
        high = v113_files[name]
        low_bytes = low.read_bytes()
        high_bytes = high.read_bytes()
        if low_bytes != high_bytes:
            fail(f"VFS mirror differs: {name}")

        try:
            root = ET.fromstring(low_bytes)
        except ET.ParseError as exc:
            fail(f"malformed XML {name}: {exc}")

        if root.tag != "TAUNTS":
            fail(f"unexpected root tag in {name}: {root.tag}")

        text = low_bytes.decode("utf-8-sig")
        if "<szTextCensored>" in text:
            warnings.append(f"{name}: legacy szTextCensored tag will be normalized by install.ps1")

        for taunt in root.findall("TAUNT"):
            if len(taunt.findall("szText")) > 1:
                index = taunt.findtext("uiIndex", default="?")
                warnings.append(f"{name}: uiIndex {index} has duplicate szText; install.ps1 treats the second as censored text")

    print(f"OK: {len(data_files)} EnemyTaunts XML files mirrored identically in Data and Data-1.13")
    print("OK: no loose civ*.edt placeholders are shipped")
    for warning in warnings:
        print(f"WARN: {warning}")


if __name__ == "__main__":
    main()
