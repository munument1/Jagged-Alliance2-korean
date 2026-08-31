#!/usr/bin/env python3
"""Verify the r7609 Korean patch localization resource manifest.

This checks the translated runtime resources that are easy to omit during packaging:
BASE/1.13 MercEdt (including snitch subfolders), translated BinaryData EDTs,
and the active NPC EDT overrides. It also validates MercEdt record structure,
confirms that every MercEdt file contains Korean text, and rejects case-colliding
paths that would collapse to one filename on Windows.
"""

from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]


def direct_edt(root: Path) -> dict[str, Path]:
    files = [
        p for p in root.iterdir()
        if p.is_file() and p.suffix.lower() == ".edt"
    ]
    folded: dict[str, list[Path]] = {}
    for path in files:
        folded.setdefault(path.name.casefold(), []).append(path)
    collisions = {
        key: paths for key, paths in folded.items()
        if len(paths) > 1
    }
    assert not collisions, {
        key: [str(path) for path in paths]
        for key, paths in collisions.items()
    }
    return {p.name.upper(): p for p in files}


def assert_no_case_collisions(root: Path, label: str) -> None:
    folded: dict[str, list[Path]] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        folded.setdefault(rel.casefold(), []).append(path)
    collisions = {
        key: paths for key, paths in folded.items()
        if len(paths) > 1
    }
    print(f"{label}_CASE_COLLISIONS={len(collisions)}")
    assert not collisions, {
        key: [str(path) for path in paths]
        for key, paths in collisions.items()
    }


def assert_manifest(root: Path, expected_sizes: dict[str, int], label: str) -> None:
    actual = direct_edt(root)
    expected = set(expected_sizes)
    missing = sorted(expected - set(actual))
    extra = sorted(set(actual) - expected)

    print(f"{label}_EXPECTED={len(expected)}")
    print(f"{label}_ACTUAL={len(actual)}")
    print(f"{label}_MISSING={missing}")
    print(f"{label}_EXTRA={extra}")

    assert not missing, (label, "missing", missing)
    assert not extra, (label, "extra", extra)

    for name, expected_size in sorted(expected_sizes.items()):
        actual_size = actual[name].stat().st_size
        assert actual_size == expected_size, (
            label,
            name,
            actual_size,
            expected_size,
        )

    print(f"{label}_SIZE_MATCH=OK")


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


def verify_recursive_merc(root: Path, label: str, expected_count: int) -> None:
    files = sorted(
        p
        for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() == ".edt"
    )
    assert len(files) == expected_count, (label, len(files), expected_count)
    for path in files:
        data = path.read_bytes()
        assert len(data) % 480 == 0, (path, len(data))
        texts = [
            decode_record(data[offset : offset + 480])
            for offset in range(0, len(data), 480)
        ]
        nonempty = [text for text in texts if text]
        hangul = [
            text
            for text in nonempty
            if any("가" <= char <= "힣" for char in text)
        ]
        assert nonempty, path
        assert hangul, (path, len(nonempty))

    print(f"{label}_RECURSIVE_EDT={len(files)}")
    print(f"{label}_STRUCTURE_AND_HANGUL=OK")


def assert_file_sizes(root: Path, manifest: dict[str, int], label: str) -> None:
    for name, expected_size in manifest.items():
        path = root / name
        assert path.is_file(), path
        actual_size = path.stat().st_size
        assert actual_size == expected_size, (path, actual_size, expected_size)
    print(f"{label}={len(manifest)}/{len(manifest)}")


def main() -> None:
    base_merc = ROOT / "Patch/Data/MercEdt"
    v113_merc = ROOT / "Patch/Data-1.13/MercEdt"

    assert_no_case_collisions(base_merc, "BASE_MERCEDT")
    assert_no_case_collisions(v113_merc, "V113_MERCEDT")

    # Effective BASE MercEdt runtime manifest, re-audited 2026-08-31.
    base_names = {f"{i:03d}.EDT" for i in range(63)} | {
        "063.EDT",
        "064.EDT",
        "066.EDT",
        "067.EDT",
        "068.EDT",
        "069.EDT",
        "070.EDT",
        "072.EDT",
        "149.EDT",
        "165.EDT",
        "166.EDT",
        "167.EDT",
        "168.EDT",
        "169.EDT",
    }
    base_sizes = {name: 56160 for name in base_names}
    base_sizes["005.EDT"] = 56640
    for number in ("032", "064", "165", "166", "168"):
        base_sizes[f"{number}.EDT"] = 68640
    for number in ("040", "046", "149", "169"):
        base_sizes[f"{number}.EDT"] = 37920
    for number in ("041", "042", "043", "044", "045", "047", "048", "049", "050"):
        base_sizes[f"{number}.EDT"] = 55200
    for number in range(51, 63):
        base_sizes[f"{number:03d}.EDT"] = 57600
    for number in ("063", "066", "067", "068", "069", "070", "072"):
        base_sizes[f"{number}.EDT"] = 38400
    assert len(base_sizes) == 77
    assert_manifest(base_merc, base_sizes, "BASE_MERCEDT")

    base_snitch = direct_edt(base_merc / "snitch")
    assert set(base_snitch) == {"023.EDT"}, sorted(base_snitch)
    assert base_snitch["023.EDT"].stat().st_size == 4320
    print("BASE_SNITCH=1/1")

    # Google Drive Data-1.13/MercEdt source manifest, re-audited 2026-08-31.
    numbers_113 = {
        4,
        13,
        14,
        15,
        20,
        31,
        37,
        40,
        149,
        167,
        169,
        *range(170, 199),
        *range(220, 254),
    }
    names_113 = {f"{number:03d}.EDT" for number in numbers_113}
    sizes_113 = {name: 56160 for name in names_113}
    for number in (
        40,
        149,
        169,
        178,
        179,
        180,
        181,
        182,
        183,
        184,
        185,
        188,
        189,
        190,
        195,
        196,
        197,
        198,
        220,
        221,
        224,
        225,
        226,
        227,
        229,
        244,
        247,
        249,
        252,
        253,
    ):
        sizes_113[f"{number:03d}.EDT"] = 37920
    sizes_113["191.EDT"] = 48960
    for number in (192, 193, 194):
        sizes_113[f"{number:03d}.EDT"] = 55200
    sizes_113["222.EDT"] = 43680
    assert len(sizes_113) == 74
    assert_manifest(v113_merc, sizes_113, "V113_MERCEDT")

    expected_snitch_113 = {
        "180.EDT",
        "187.EDT",
        "188.EDT",
        "222.EDT",
        "223.EDT",
        "225.EDT",
        "227.EDT",
        "240.EDT",
        "249.EDT",
    }
    snitch_113 = direct_edt(v113_merc / "snitch")
    assert set(snitch_113) == expected_snitch_113, (
        sorted(snitch_113),
        sorted(expected_snitch_113),
    )
    assert all(path.stat().st_size == 4320 for path in snitch_113.values())
    print("V113_SNITCH=9/9")

    assert_file_sizes(
        ROOT / "Patch/Data/BinaryData",
        {
            "AIMHIST.EDT": 18400,
            "AIMPOL.EDT": 36800,
            "ALUMNAME.EDT": 8160,
            "ALUMNI.EDT": 65280,
            "CREDITS.EDT": 39680,
            "FILES.EDT": 57600,
            "FLOWERCARD.EDT": 7200,
            "FLOWERDESC.EDT": 9600,
            "HELP.EDT": 157440,
            "IMPASS.EDT": 146560,
            "IMPTEXT.EDT": 191200,
            "INSURANCEMULTI.EDT": 28800,
            "INSURANCESINGLE.EDT": 4800,
            "QUESTS.EDT": 7360,
            "RIS.EDT": 54400,
        },
        "BASE_BINARY_TRANSLATED",
    )

    assert_file_sizes(
        ROOT / "Patch/Data-1.13/BinaryData",
        {
            "AIMBIOS.EDT": 79520,
            "EMAIL.EDT": 149120,
            "MERCBIOS.EDT": 48160,
        },
        "V113_BINARY_TRANSLATED",
    )

    # The BASE source has an old 159.EDT, but r7609 resolves Data-1.13 above
    # Data. The translated Data-1.13/NpcData/159.EDT is the intended runtime
    # override, so BASE 159 is deliberately not required here.
    assert_file_sizes(
        ROOT / "Patch/Data/NPCData",
        {
            "097.EDT": 27840,
            "138.EDT": 13440,
            "civ52.edt": 4800,
            "H8.edt": 960,
        },
        "BASE_NPC_DRIVE_RUNTIME_SUBSET",
    )

    assert_file_sizes(
        ROOT / "Patch/Data-1.13/NpcData",
        {
            "159.EDT": 42240,
            "229.EDT": 12960,
        },
        "V113_NPC_TRANSLATED",
    )
    print("BASE_159_VFS_OVERRIDE=Data-1.13/NpcData/159.EDT")

    verify_recursive_merc(base_merc, "BASE_MERCEDT", 78)
    verify_recursive_merc(v113_merc, "V113_MERCEDT", 83)

    base_rel = {
        path.relative_to(base_merc).as_posix().lower()
        for path in base_merc.rglob("*")
        if path.is_file() and path.suffix.lower() == ".edt"
    }
    v113_rel = {
        path.relative_to(v113_merc).as_posix().lower()
        for path in v113_merc.rglob("*")
        if path.is_file() and path.suffix.lower() == ".edt"
    }
    overlap = base_rel & v113_rel
    expected_overlap = {
        "004.edt",
        "013.edt",
        "014.edt",
        "015.edt",
        "020.edt",
        "031.edt",
        "037.edt",
        "040.edt",
        "149.edt",
        "167.edt",
        "169.edt",
    }
    assert overlap == expected_overlap, (sorted(overlap), sorted(expected_overlap))
    print(f"MERCEDT_VFS_OVERLAP_COUNT={len(overlap)}")
    print("MERCEDT_VFS_OVERLAP=" + ",".join(sorted(overlap)))
    print("LOCALIZATION_PACKAGE_MANIFEST=OK")


if __name__ == "__main__":
    main()
