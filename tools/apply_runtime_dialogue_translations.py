#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "qa"
MAPPING_GLOB = "runtime_dialogue_ko_*.tsv"
EXPECTED_TRANSLATIONS = 239
MIRROR_MERC_IDS = ("004", "013", "014", "015", "020", "031", "037", "040", "149", "167", "169")


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


def load_mappings() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for path in sorted(QA.glob(MAPPING_GLOB)):
        with path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh, delimiter="\t")
            for row in reader:
                key = (row["Path"], row["Record"], row["Mode"])
                if key in seen:
                    raise ValueError(f"duplicate mapping: {key}")
                seen.add(key)
                rows.append(row)
    if len(rows) != EXPECTED_TRANSLATIONS:
        raise ValueError(f"expected {EXPECTED_TRANSLATIONS} translations, found {len(rows)}")
    return rows


def patch_fixed(path: Path, record: int, text: str) -> None:
    size = 480
    data = bytearray(path.read_bytes())
    offset = (record - 1) * size
    if offset < 0 or offset + size > len(data):
        raise ValueError(f"record {record} outside {path} ({len(data)} bytes)")
    data[offset:offset + size] = encode_record(text, size)
    path.write_bytes(data)


def patch_mercbios_bio(path: Path, profile: int, text: str) -> None:
    stride = 1120
    size = 800
    data = bytearray(path.read_bytes())
    offset = (profile - 1) * stride
    if offset < 0 or offset + size > len(data):
        raise ValueError(f"profile {profile} outside {path} ({len(data)} bytes)")
    data[offset:offset + size] = encode_record(text, size)
    path.write_bytes(data)


def mirror_base_mercs() -> None:
    source_dir = ROOT / "Patch" / "Data" / "MercEdt"
    target_dir = ROOT / "Patch" / "Data-1.13" / "MercEdt"
    target_dir.mkdir(parents=True, exist_ok=True)
    for merc_id in MIRROR_MERC_IDS:
        candidates = list(source_dir.glob(f"{merc_id}.[Ee][Dd][Tt]"))
        if len(candidates) != 1:
            raise ValueError(f"expected one base MercEdt for {merc_id}, found {candidates}")
        target = target_dir / f"{merc_id}.EDT"
        shutil.copyfile(candidates[0], target)
        print(f"MIRROR {candidates[0].relative_to(ROOT)} -> {target.relative_to(ROOT)}")


def main() -> None:
    rows = load_mappings()
    for row in rows:
        path = ROOT / row["Path"]
        record = int(row["Record"])
        mode = row["Mode"]
        text = row["Korean"]
        if mode == "fixed":
            patch_fixed(path, record, text)
        elif mode == "mercbios_bio":
            patch_mercbios_bio(path, record, text)
        else:
            raise ValueError(f"unsupported mapping mode: {mode}")
        print(f"PATCH {row['Path']} record={record} mode={mode}")

    # Apply the corrected base 149 first, then mirror it together with the other
    # known Korean base mercs into the higher-priority Data-1.13 layer.
    mirror_base_mercs()
    print(f"PATCHED_TRANSLATIONS={len(rows)}")
    print(f"MIRRORED_MERCS={len(MIRROR_MERC_IDS)}")


if __name__ == "__main__":
    main()
