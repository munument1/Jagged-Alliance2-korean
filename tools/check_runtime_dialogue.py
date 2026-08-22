#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_TAUNTS = ROOT / "Patch" / "Data" / "TableData" / "EnemyTaunts"
V113_TAUNTS = ROOT / "Patch" / "Data-1.13" / "TableData" / "EnemyTaunts"
NPCDATA = ROOT / "Patch" / "Data" / "NPCData"

# v0.1.4-alpha completed the BASE civilian dialogue set. The pre-v0.1.4
# validator expected only civ52.edt and therefore became stale once civ00-39
# were intentionally added to the release payload.
EXPECTED_CIV_NAMES = {f"civ{i:02d}.edt" for i in range(40)} | {"civ52.edt"}
VERIFIED_CIV_SHA = {
    "civ52.edt": "1b52df9618f9a52288739b516148035e083ecc02",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> None:
    civ_files = {
        p.name.lower(): p
        for p in NPCDATA.iterdir()
        if p.is_file() and p.name.lower().startswith("civ") and p.suffix.lower() == ".edt"
    }
    if set(civ_files) != EXPECTED_CIV_NAMES:
        fail(
            "unexpected CIV EDT set; expected="
            + repr(sorted(EXPECTED_CIV_NAMES))
            + ", actual="
            + repr(sorted(civ_files))
        )

    for name, expected_sha in VERIFIED_CIV_SHA.items():
        actual_sha = git_blob_sha(civ_files[name].read_bytes())
        if actual_sha != expected_sha:
            fail(f"verified CIV EDT changed unexpectedly: {name}: {actual_sha}")

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
        if "<szTextCensored>" in text or "</szTextCensored>" in text:
            fail(f"legacy szTextCensored tag remains in {name}")

        for taunt in root.findall("TAUNT"):
            index = taunt.findtext("uiIndex", default="?")
            if len(taunt.findall("szText")) != 1:
                fail(f"{name}: uiIndex {index} must contain exactly one szText")
            if len(taunt.findall("szCensoredText")) > 1:
                fail(f"{name}: uiIndex {index} contains duplicate szCensoredText")

    print(f"OK: {len(data_files)} EnemyTaunts XML files mirrored identically in Data and Data-1.13")
    print("OK: EnemyTaunts censorship tags and text-node structure are normalized")
    print(f"OK: complete BASE civilian EDT set present ({len(EXPECTED_CIV_NAMES)} files)")


if __name__ == "__main__":
    main()
