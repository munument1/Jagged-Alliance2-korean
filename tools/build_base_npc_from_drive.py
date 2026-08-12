#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import struct
import urllib.request
from collections import defaultdict
from pathlib import Path

DRIVE_FILE_ID = "1DXc1g-D6z7MYvrI_XjXDeS0OtYQpttCv"
SOURCE_URL = f"https://drive.usercontent.google.com/download?id={DRIVE_FILE_ID}&export=download&confirm=t"
EXPECTED_SHA256 = "93dc2209570ed17e405acd64c0b1ace1e3710c7a9bc627c43913c1494c2f0a0a"
EXPECTED_ROWS = 3434
EXPECTED_TRANSLATED = 3233
EXPECTED_BLANK = 201
EXPECTED_FILES = 160


def encode_record(text: str, size: int) -> bytes:
    units: list[int] = []
    for ch in text:
        value = ord(ch)
        if value > 0xFFFF:
            raise ValueError(f"non-BMP character is not supported by JA2 EDT: {ch!r}")
        if value > 32:
            value += 1
        units.append(value)
    units.append(0)
    raw = struct.pack("<" + "H" * len(units), *units)
    if len(raw) > size:
        raise ValueError(f"translation needs {len(raw)} bytes but record size is {size}: {text}")
    return raw + b"\x00" * (size - len(raw))


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


def get_source(source: Path | None, temp_path: Path) -> Path:
    if source is not None:
        shutil.copyfile(source, temp_path)
        return temp_path
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as response, temp_path.open("wb") as out:
        shutil.copyfileobj(response, out)
    return temp_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="Use a local TSV instead of downloading from Drive")
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--source-copy",
        type=Path,
        default=Path("qa/JA2_r7609_BASE_NPC_Translation_Queue_FINAL.tsv"),
        help="Path under output-root where the verified TSV is preserved",
    )
    args = parser.parse_args()

    root = args.output_root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    temp_path = root / ".base_npc_translation_download.tsv"
    get_source(args.source, temp_path)

    digest = hashlib.sha256(temp_path.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(f"translation source SHA-256 mismatch: {digest}")

    with temp_path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))

    if len(rows) != EXPECTED_ROWS:
        raise ValueError(f"expected {EXPECTED_ROWS} rows, found {len(rows)}")
    translated = [row for row in rows if row["English"]]
    blank = [row for row in rows if not row["English"]]
    if len(translated) != EXPECTED_TRANSLATED or len(blank) != EXPECTED_BLANK:
        raise ValueError(f"unexpected translated/blank counts: {len(translated)}/{len(blank)}")
    if any(not row["Korean"] or row["Status"] != "번역완료" for row in translated):
        raise ValueError("a nonblank English row is missing a completed Korean translation")
    if any(row["Korean"] for row in blank):
        raise ValueError("an originally blank row unexpectedly contains Korean text")

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        path = row["Path"]
        if not path.startswith("Data/NPCData/"):
            raise ValueError(f"unexpected path outside BASE NPCData: {path}")
        grouped[path].append(row)
    if len(grouped) != EXPECTED_FILES:
        raise ValueError(f"expected {EXPECTED_FILES} EDT files, found {len(grouped)}")

    manifest_files: list[dict[str, object]] = []
    for rel_path, file_rows in sorted(grouped.items()):
        file_rows.sort(key=lambda row: int(row["Record"]))
        records = [int(row["Record"]) for row in file_rows]
        if records != list(range(1, len(file_rows) + 1)):
            raise ValueError(f"non-contiguous records in {rel_path}")
        sizes = {int(row["RecordBytes"]) for row in file_rows}
        if len(sizes) != 1:
            raise ValueError(f"mixed record sizes in {rel_path}: {sizes}")
        size = next(iter(sizes))
        if size not in (320, 480):
            raise ValueError(f"unexpected record size {size} in {rel_path}")

        encoded = bytearray()
        for row in file_rows:
            record = encode_record(row["Korean"], size)
            if decode_record(record) != row["Korean"]:
                raise ValueError(f"round-trip mismatch in {rel_path} record {row['Record']}")
            encoded.extend(record)

        target = root / "Patch" / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(encoded)
        manifest_files.append({
            "path": rel_path,
            "records": len(file_rows),
            "record_bytes": size,
            "file_bytes": len(encoded),
            "sha256": hashlib.sha256(encoded).hexdigest(),
        })

    source_copy = root / args.source_copy
    source_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(temp_path, source_copy)
    temp_path.unlink(missing_ok=True)

    manifest = {
        "version": "v0.1.4-alpha",
        "source_drive_file_id": DRIVE_FILE_ID,
        "source_sha256": EXPECTED_SHA256,
        "rows": EXPECTED_ROWS,
        "translated": EXPECTED_TRANSLATED,
        "blank": EXPECTED_BLANK,
        "files": manifest_files,
    }
    manifest_path = root / "qa" / "base_npc_v014_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"BASE_NPC_FILES={len(manifest_files)}")
    print(f"BASE_NPC_RECORDS={len(rows)}")
    print(f"BASE_NPC_TRANSLATED={len(translated)}")
    print(f"BASE_NPC_BLANK={len(blank)}")
    print("BASE_NPC_QA=PASS")


if __name__ == "__main__":
    main()
