#!/usr/bin/env python3
"""
Apply the Korean r7609 runtime hotfixes to an upstream 1dot13/source checkout.

Baseline:
  repository: https://github.com/1dot13/source
  commit: af1f5c5e173382b5070494e3414bcf5145fd9a6b
  SVN marker: Build@7606 (last source change before r7609)

Hotfixes:
  1) Allow Hangul characters in the I.M.P. full-name/nickname input filter.
  2) Expand Fleuropa/Florist destination mouse hitboxes for WinFont builds and
     raise the closed dropdown's activation-region priority by one level.

The script deliberately patches only the two known source files and refuses to
continue if the expected baseline snippets are not found.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

BASELINE_COMMIT = "af1f5c5e173382b5070494e3414bcf5145fd9a6b"


@dataclass(frozen=True)
class Replacement:
    path: str
    label: str
    old_lf: str
    new_lf: str


REPLACEMENTS = (
    Replacement(
        path="Laptop/IMP Begin Screen.cpp",
        label="I.M.P. Hangul name input",
        old_lf="""\
\t#ifndef USE_CODE_PAGE
\t\tif( uiKey >= 'A' && uiKey <= 'Z' ||
\t\t\t\t\tuiKey >= 'a' && uiKey <= 'z' ||
\t\t\t\t\tuiKey >= '0' && uiKey <= '9' ||
\t\t\t\t\tuiKey == '_' || uiKey == '.' ||
\t\t\t\t\tuiKey == ' ' || uiKey == '\\"' ||
\t\t\t\t\tuiKey == 39 // This is ' which cannot be written explicitly here of course
\t\t\t\t\t)
\t#else
\t\tif( charSet::IsFromSet( uiKey, charSet::CS_SPACE|charSet::CS_ALPHA_NUM|charSet::CS_SPECIAL_ALPHA ) )
\t#endif
""",
        new_lf="""\
\t#ifndef USE_CODE_PAGE
\t\tif( uiKey >= 'A' && uiKey <= 'Z' ||
\t\t\t\t\tuiKey >= 'a' && uiKey <= 'z' ||
\t\t\t\t\tuiKey >= '0' && uiKey <= '9' ||
\t\t\t\t\tuiKey == '_' || uiKey == '.' ||
\t\t\t\t\tuiKey == ' ' || uiKey == '\\"' ||
\t\t\t\t\tuiKey == 39 || // This is ' which cannot be written explicitly here of course
\t\t\t\t\t( uiKey >= 0x1100 && uiKey <= 0x11FF ) || // Hangul Jamo
\t\t\t\t\t( uiKey >= 0x3130 && uiKey <= 0x318F ) || // Hangul Compatibility Jamo
\t\t\t\t\t( uiKey >= 0xAC00 && uiKey <= 0xD7A3 )    // Hangul Syllables
\t\t\t\t\t)
\t#else
\t\tif( charSet::IsFromSet( uiKey, charSet::CS_SPACE|charSet::CS_ALPHA_NUM|charSet::CS_SPECIAL_ALPHA ) ||
\t\t\t\t\t( uiKey >= 0x1100 && uiKey <= 0x11FF ) ||
\t\t\t\t\t( uiKey >= 0x3130 && uiKey <= 0x318F ) ||
\t\t\t\t\t( uiKey >= 0xAC00 && uiKey <= 0xD7A3 ) )
\t#endif
""",
    ),
    Replacement(
        path="Laptop/florist Order Form.cpp",
        label="Florist destination activation priority",
        old_lf="""\
\tMSYS_DefineRegion( &gSelectedFloristDropDownRegion, FLOWER_ORDER_DELIVERY_LOCATION_X, FLOWER_ORDER_DELIVERY_LOCATION_Y, (UINT16)(FLOWER_ORDER_DELIVERY_LOCATION_X + FLOWER_ORDER_DELIVERY_LOCATION_WIDTH), (UINT16)(FLOWER_ORDER_DELIVERY_LOCATION_Y + FLOWER_ORDER_DELIVERY_LOCATION_HEIGHT), MSYS_PRIORITY_HIGH,
""",
        new_lf="""\
\tMSYS_DefineRegion( &gSelectedFloristDropDownRegion, FLOWER_ORDER_DELIVERY_LOCATION_X, FLOWER_ORDER_DELIVERY_LOCATION_Y, (UINT16)(FLOWER_ORDER_DELIVERY_LOCATION_X + FLOWER_ORDER_DELIVERY_LOCATION_WIDTH), (UINT16)(FLOWER_ORDER_DELIVERY_LOCATION_Y + FLOWER_ORDER_DELIVERY_LOCATION_HEIGHT), MSYS_PRIORITY_HIGH+1,
""",
    ),
    Replacement(
        path="Laptop/florist Order Form.cpp",
        label="Florist destination row hitboxes",
        old_lf="""\
\t\t\t\tMSYS_DefineRegion( &gSelectedFlowerDropDownRegion[i], usPosX, (UINT16)(usPosY+4), (UINT16)(usPosX+FLOWER_ORDER_DROP_DOWN_LOCATION_WIDTH), (UINT16)(usPosY+usFontHeight), MSYS_PRIORITY_HIGH+3,
""",
        new_lf="""\
\t\t\t\t// WinFont can report a taller glyph box than the legacy bitmap font.
\t\t\t\t// Cover the whole visual row instead of leaving only a narrow click strip.
\t\t\t\tMSYS_DefineRegion( &gSelectedFlowerDropDownRegion[i], usPosX, usPosY, (UINT16)(usPosX+FLOWER_ORDER_DROP_DOWN_LOCATION_WIDTH), (UINT16)(usPosY+usFontHeight+2), MSYS_PRIORITY_HIGH+3,
""",
    ),
)


def detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def with_newline(text_lf: str, newline: str) -> str:
    return text_lf.replace("\n", newline)


def load_lossless(path: Path) -> str:
    # latin-1 is a 1:1 byte mapping, so unrelated legacy-source bytes survive.
    return path.read_bytes().decode("latin-1")


def save_lossless(path: Path, text: str) -> None:
    path.write_bytes(text.encode("latin-1"))


def patch_one(source_root: Path, replacement: Replacement, check_only: bool) -> str:
    path = source_root / replacement.path
    if not path.is_file():
        raise RuntimeError(f"missing source file: {path}")

    text = load_lossless(path)
    newline = detect_newline(text)
    old = with_newline(replacement.old_lf, newline)
    new = with_newline(replacement.new_lf, newline)

    if new in text:
        return f"OK already applied: {replacement.label}"

    if old not in text:
        raise RuntimeError(
            f"baseline mismatch for {replacement.label}: expected snippet was not found in {path}\n"
            f"Expected upstream baseline: 1dot13/source@{BASELINE_COMMIT}"
        )

    if check_only:
        raise RuntimeError(f"NOT APPLIED: {replacement.label}")

    if text.count(old) != 1:
        raise RuntimeError(
            f"refusing ambiguous replacement for {replacement.label}: "
            f"found {text.count(old)} matches in {path}"
        )

    text = text.replace(old, new, 1)
    save_lossless(path, text)
    return f"APPLIED: {replacement.label}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source_root",
        type=Path,
        help="root of the 1dot13/source checkout (contains Laptop/)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that all hotfixes are already present; do not modify files",
    )
    args = parser.parse_args()

    source_root = args.source_root.resolve()

    try:
        messages = [
            patch_one(source_root, replacement, args.check)
            for replacement in REPLACEMENTS
        ]
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for message in messages:
        print(message)

    if args.check:
        print("All r7609 Korean runtime hotfixes are present.")
    else:
        print("Hotfix application complete.")
        print("Run again with --check before building.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
