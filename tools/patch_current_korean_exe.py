#!/usr/bin/env python3
"""Patch the currently shipped Korean r7609 ja2.exe without rebuilding it.

This is intentionally tied to the exact Korean executable currently stored at
Patch/ja2.exe. It preserves all compiled Korean UI strings and earlier WinFont
layout fixes while changing only the machine-code bytes needed for:

1. I.M.P. Unicode/Hangul name input.
2. Fleuropa florist destination row hitboxes.

The patcher refuses unknown executables and verifies every byte signature before
writing anything. It can also migrate the first reviewed test build to the final
non-overlapping florist hitbox build.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

ORIGINAL_SHA256 = "5da88f00f4cc9087463c98dab7594cf14379cf1aa281ef835296bac0fcd10582"
PREVIOUS_PATCHED_SHA256 = "5087524fa181064a7c4646acee9b96cabb3ded68080a2662a6b242a021eb8ea1"
PATCHED_SHA256 = "a3480fd92a6c5e4e184b367cf29705d52b8b129a616c6a6a80affd062ee77582"
EXPECTED_SIZE = 8_407_552


@dataclass(frozen=True)
class Patch:
    label: str
    offset: int
    old: bytes
    new: bytes
    previous: bytes | None = None


PATCHES = (
    Patch(
        label="Florist row Y-bias: expand hitbox without row overlap",
        offset=0x0F5230,
        old=bytes.fromhex("D3"),
        previous=bytes.fromhex("D7"),
        new=bytes.fromhex("D5"),
    ),
    Patch(
        label="Florist row top: align click start with visual row",
        offset=0x0F5278,
        old=bytes.fromhex("04"),
        previous=bytes.fromhex("FC"),
        new=bytes.fromhex("FE"),
    ),
    Patch(
        label="Florist dropdown height: cancel internal Y-bias",
        offset=0x0F52E3,
        old=bytes.fromhex("C9"),
        previous=bytes.fromhex("CD"),
        new=bytes.fromhex("CB"),
    ),
    Patch(
        label="I.M.P. name input: preserve ASCII rules and accept Unicode >= U+0100",
        offset=0x12B6BD,
        old=bytes.fromhex(
            "83 F8 5F 74 18 83 F8 2E 74 13 83 F8 20 74 0E "
            "83 F8 22 74 09 83 F8 27 0F 85 C5 00 00 00"
        ),
        previous=bytes.fromhex(
            "84 E4 75 19 3C 5F 74 15 3C 2E 74 11 3C 20 74 0D "
            "3C 22 74 09 3C 27 0F 85 C6 00 00 00 90"
        ),
        new=bytes.fromhex(
            "84 E4 75 19 3C 5F 74 15 3C 2E 74 11 3C 20 74 0D "
            "3C 22 74 09 3C 27 0F 85 C6 00 00 00 90"
        ),
    ),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def expected_bytes(patch: Patch, state: str) -> bytes:
    if state == "original":
        return patch.old
    if state == "previous":
        return patch.previous if patch.previous is not None else patch.new
    if state == "patched":
        return patch.new
    raise ValueError(state)


def check_signatures(data: bytes, state: str) -> None:
    for patch in PATCHES:
        expected = expected_bytes(patch, state)
        actual = data[patch.offset : patch.offset + len(expected)]
        if actual != expected:
            raise RuntimeError(
                f"{patch.label}: {state} byte signature mismatch at 0x{patch.offset:08X}\n"
                f"expected: {expected.hex(' ')}\n"
                f"actual:   {actual.hex(' ')}"
            )


def apply(data: bytes) -> bytes:
    if len(data) != EXPECTED_SIZE:
        raise RuntimeError(
            f"unexpected executable size: {len(data)} bytes (expected {EXPECTED_SIZE})"
        )

    digest = sha256(data)
    if digest == PATCHED_SHA256:
        check_signatures(data, "patched")
        return data
    if digest == PREVIOUS_PATCHED_SHA256:
        check_signatures(data, "previous")
        state = "previous"
    elif digest == ORIGINAL_SHA256:
        check_signatures(data, "original")
        state = "original"
    else:
        raise RuntimeError(
            "refusing to patch an unknown ja2.exe\n"
            f"expected original SHA-256: {ORIGINAL_SHA256}\n"
            f"expected previous test SHA-256: {PREVIOUS_PATCHED_SHA256}\n"
            f"actual SHA-256: {digest}"
        )

    patched = bytearray(data)
    for patch in PATCHES:
        old_bytes = expected_bytes(patch, state)
        patched[patch.offset : patch.offset + len(old_bytes)] = patch.new

    result = bytes(patched)
    check_signatures(result, "patched")
    digest = sha256(result)
    if digest != PATCHED_SHA256:
        raise RuntimeError(
            "patched executable hash did not match the reviewed build\n"
            f"expected: {PATCHED_SHA256}\n"
            f"actual:   {digest}"
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="current Korean Patch/ja2.exe")
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        help="output path; omit with --check or use --in-place",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that the executable is an exact recognized build",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="replace the input file after successful validation and patching",
    )
    args = parser.parse_args()

    try:
        data = args.input.read_bytes()
        digest = sha256(data)

        if args.check:
            if digest == ORIGINAL_SHA256:
                check_signatures(data, "original")
                print(f"ORIGINAL OK  {digest}  {args.input}")
                return 0
            if digest == PREVIOUS_PATCHED_SHA256:
                check_signatures(data, "previous")
                print(f"PREVIOUS TEST OK  {digest}  {args.input}")
                return 0
            if digest == PATCHED_SHA256:
                check_signatures(data, "patched")
                print(f"PATCHED OK   {digest}  {args.input}")
                return 0
            raise RuntimeError(f"unknown executable SHA-256: {digest}")

        if args.in_place and args.output is not None:
            raise RuntimeError("do not combine an output path with --in-place")
        if not args.in_place and args.output is None:
            raise RuntimeError("provide an output path or use --in-place")

        result = apply(data)
        if digest == PATCHED_SHA256:
            print("Executable is already patched; no byte changes needed.")

        if args.in_place:
            temp = args.input.with_suffix(args.input.suffix + ".runtime-hotfix.tmp")
            temp.write_bytes(result)
            shutil.copymode(args.input, temp)
            temp.replace(args.input)
            target = args.input
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(result)
            shutil.copymode(args.input, args.output)
            target = args.output

        print(f"PATCHED OK   {sha256(result)}  {target}")
        print("Changed machine-code bytes from original: 27")
        return 0
    except (OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
