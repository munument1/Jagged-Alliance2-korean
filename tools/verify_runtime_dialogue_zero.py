#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qa" / "runtime_dialogue_final_audit.tsv"


def decode_record(raw: bytes) -> str:
    values = struct.unpack("<" + "H" * (len(raw) // 2), raw)
    chars: list[str] = []
    for value in values:
        if value == 0:
            break
        if value > 33:
            value -= 1
        chars.append(chr(value))
    return "".join(chars)


def looks_untranslated(text: str) -> bool:
    if not text.strip():
        return False
    words = re.findall(r"[A-Za-z]{2,}", text)
    if not words:
        return False
    latin = sum(ch.isascii() and ch.isalpha() for ch in text)
    hangul = sum("가" <= ch <= "힣" for ch in text)
    return latin >= 3 and (hangul == 0 or latin > hangul * 2)


def iter_edt(folder: Path):
    seen: set[Path] = set()
    for pattern in ("*.edt", "*.EDT"):
        for path in sorted(folder.rglob(pattern), key=lambda p: str(p).lower()):
            if path not in seen:
                seen.add(path)
                yield path


def scan_fixed(path: Path, record_bytes: int, family: str, rows: list[list[str]]) -> None:
    data = path.read_bytes()
    actual = record_bytes
    if len(data) % actual:
        if record_bytes == 320 and len(data) % 480 == 0:
            actual = 480
        else:
            rows.append([family, str(path.relative_to(ROOT)), "FILE", "", f"UNRECOGNIZED_SIZE_{len(data)}"])
            return
    for record, offset in enumerate(range(0, len(data), actual), 1):
        text = decode_record(data[offset:offset + actual])
        if looks_untranslated(text):
            rows.append([family, str(path.relative_to(ROOT)), str(record), f"0x{offset:08X}", text])


def scan_mercbios(path: Path, rows: list[list[str]]) -> None:
    data = path.read_bytes()
    stride = 1120
    if len(data) % stride:
        rows.append(["MERCBIOS", str(path.relative_to(ROOT)), "FILE", "", f"UNRECOGNIZED_SIZE_{len(data)}"])
        return
    for profile, base in enumerate(range(0, len(data), stride), 1):
        for kind, rel, size in (("bio", 0, 800), ("additional", 800, 320)):
            text = decode_record(data[base + rel:base + rel + size])
            if looks_untranslated(text):
                rows.append([f"MERCBIOS:{kind}", str(path.relative_to(ROOT)), str(profile), f"0x{base + rel:08X}", text])


def scan_enemy_taunts(folder: Path, rows: list[list[str]]) -> None:
    if not folder.exists():
        return
    for path in sorted(folder.glob("EnemyTaunts*.xml")):
        root = ET.parse(path).getroot()
        for taunt in root.findall("TAUNT"):
            index = taunt.findtext("uiIndex", default="?")
            for tag in ("szText", "szCensoredText"):
                node = taunt.find(tag)
                if node is not None and node.text and looks_untranslated(node.text):
                    rows.append([f"EnemyTaunts:{tag}", str(path.relative_to(ROOT)), index, "", node.text])


def main() -> int:
    rows: list[list[str]] = []
    for folder in (
        ROOT / "Patch" / "Data" / "MercEdt",
        ROOT / "Patch" / "Data-1.13" / "MercEdt",
    ):
        if folder.exists():
            for path in iter_edt(folder):
                scan_fixed(path, 480, "MercEdt", rows)

    for folder in (
        ROOT / "Patch" / "Data" / "NPCData",
        ROOT / "Patch" / "Data-1.13" / "NpcData",
    ):
        if folder.exists():
            for path in iter_edt(folder):
                scan_fixed(path, 320, "NPCData", rows)

    for path in (
        ROOT / "Patch" / "Data" / "BinaryData" / "MERCBIOS.EDT",
        ROOT / "Patch" / "Data-1.13" / "BinaryData" / "MERCBIOS.EDT",
    ):
        if path.exists():
            scan_mercbios(path, rows)

    scan_enemy_taunts(ROOT / "Patch" / "Data" / "TableData" / "EnemyTaunts", rows)
    scan_enemy_taunts(ROOT / "Patch" / "Data-1.13" / "TableData" / "EnemyTaunts", rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
        writer.writerow(["Family", "Path", "Record", "Offset", "DecodedText"])
        writer.writerows(rows)

    print(f"RUNTIME_UNTRANSLATED={len(rows)}")
    for row in rows:
        print("\t".join(row))
    return 1 if rows else 0


if __name__ == "__main__":
    sys.exit(main())
