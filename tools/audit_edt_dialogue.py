#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qa" / "runtime_dialogue_untranslated.tsv"

# JA2 encrypted EDT: runtime DecodeString subtracts 1 from non-NUL UTF-16 code units > 33.
def decode_record(raw: bytes) -> str:
    if len(raw) % 2:
        return ""
    vals = list(struct.unpack("<" + "H" * (len(raw) // 2), raw))
    out = []
    for value in vals:
        if value == 0:
            break
        if value > 33:
            value -= 1
        out.append(chr(value))
    return "".join(out).replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")


def looks_english(text: str) -> bool:
    if not text.strip():
        return False
    # Ignore pure identifiers/numbers; require an English word of 2+ letters.
    words = re.findall(r"[A-Za-z]{2,}", text)
    if not words:
        return False
    latin = sum(ch.isascii() and ch.isalpha() for ch in text)
    hangul = sum("가" <= ch <= "힣" for ch in text)
    return latin >= 3 and (hangul == 0 or latin > hangul * 2)


def scan_fixed(path: Path, record_bytes: int, layer: str, family: str, rows: list[list[str]]) -> None:
    data = path.read_bytes()
    if len(data) % record_bytes:
        rows.append([layer, family, str(path.relative_to(ROOT)), "FILE", "", f"SIZE_NOT_MULTIPLE_OF_{record_bytes}"])
        return
    for idx, off in enumerate(range(0, len(data), record_bytes), start=1):
        text = decode_record(data[off:off + record_bytes])
        if looks_english(text):
            rows.append([layer, family, str(path.relative_to(ROOT)), str(idx), f"0x{off:08X}", text])


def scan_mercbios(path: Path, layer: str, rows: list[list[str]]) -> None:
    # AimMembers.cpp: each profile has 800-byte bio + 320-byte additional-info record.
    data = path.read_bytes()
    stride = 800 + 320
    if len(data) % stride:
        rows.append([layer, "MERCBIOS", str(path.relative_to(ROOT)), "FILE", "", f"SIZE_NOT_MULTIPLE_OF_{stride}"])
        return
    profile = 0
    for base in range(0, len(data), stride):
        profile += 1
        for kind, rel, size in (("bio", 0, 800), ("additional", 800, 320)):
            text = decode_record(data[base + rel:base + rel + size])
            if looks_english(text):
                rows.append([layer, f"MERCBIOS:{kind}", str(path.relative_to(ROOT)), str(profile), f"0x{base + rel:08X}", text])


def main() -> None:
    rows: list[list[str]] = []
    targets = [
        ("Data", ROOT / "Patch" / "Data" / "MercEdt", 480, "MercEdt"),
        ("Data-1.13", ROOT / "Patch" / "Data-1.13" / "MercEdt", 480, "MercEdt"),
        ("Data", ROOT / "Patch" / "Data" / "NPCData", 320, "NPCData"),
        ("Data-1.13", ROOT / "Patch" / "Data-1.13" / "NpcData", 320, "NPCData"),
    ]
    for layer, folder, record_bytes, family in targets:
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("*.edt"), key=lambda p: str(p).lower()):
            scan_fixed(path, record_bytes, layer, family, rows)
        for path in sorted(folder.rglob("*.EDT"), key=lambda p: str(p).lower()):
            if path.suffix == ".EDT" and not any(r[2] == str(path.relative_to(ROOT)) for r in rows if r[3] == "FILE"):
                # Avoid duplicate scan on case-insensitive glob overlap by checking exact path list below.
                pass

    # pathlib glob on Linux is case-sensitive; explicitly gather uppercase EDTs not already covered.
    for layer, folder, record_bytes, family in targets:
        if not folder.exists():
            continue
        lower_set = set(folder.rglob("*.edt"))
        for path in sorted(folder.rglob("*.EDT"), key=lambda p: str(p).lower()):
            if path not in lower_set:
                scan_fixed(path, record_bytes, layer, family, rows)

    for layer, path in (
        ("Data", ROOT / "Patch" / "Data" / "BinaryData" / "MERCBIOS.EDT"),
        ("Data-1.13", ROOT / "Patch" / "Data-1.13" / "BinaryData" / "MERCBIOS.EDT"),
    ):
        if path.exists():
            scan_mercbios(path, layer, rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
        writer.writerow(["Layer", "Family", "Path", "Record", "Offset", "DecodedText"])
        writer.writerows(rows)

    by_file: dict[str, int] = {}
    for row in rows:
        by_file[row[2]] = by_file.get(row[2], 0) + 1
    print(f"UNTRANSLATED_ROWS={len(rows)}")
    for path, count in sorted(by_file.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{count:4d}\t{path}")


if __name__ == "__main__":
    main()
