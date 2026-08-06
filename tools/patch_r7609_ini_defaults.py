from __future__ import annotations

import argparse
import re
from pathlib import Path


SETTINGS: dict[str, dict[str, dict[str, str]]] = {
    "CTHConstants.ini": {
        "General": {
            "IRON_SIGHTS_MAX_APERTURE_USE_GRADIENT": "FALSE",
        },
    },
    "Skills_Settings.INI": {
        "Covert Ops": {
            "COVERT_DETECTEDIFBLEEDING": "FALSE",
        },
    },
    "Ja2_Options.INI": {
        "Strategic Gameplay Settings": {
            "ARMY_USES_TANKS_IN_PATROLS": "FALSE",
            "ARMY_USES_TANKS_IN_ATTACKS": "FALSE",
        },
        "PMC Settings": {
            "PMC": "TRUE",
        },
        "Dynamic Dialogue Settings": {
            "DYNAMIC_DIALOGUE": "FALSE",
        },
        "Dynamic Opinion Settings": {
            "DYNAMIC_OPINIONS_SHOWCHANGE": "TRUE",
            "DYNAMIC_OPINIONS": "TRUE",
        },
        "Disease Settings": {
            "DISEASE_STRATEGIC": "FALSE",
            "DISEASE": "FALSE",
        },
        "Tactical Cover System Settings": {
            "COVER_TOOLTIP_DISPLAY_DETAILED_TILE_PROPERTIES": "TRUE",
            "COVER_SYSTEM_ALTERNATE_MULTI_TERRAIN_CAMO_CALCULATION": "TRUE",
            "COVER_SYSTEM_STATIC_SHADOWS_DECREASE_BRIGHTNESS": "FALSE",
            "COVER_SYSTEM_ADDITIONAL_TILE_PROPERTIES": "TRUE",
        },
        "Tactical Enemy Role Settings": {
            "ENEMY_GENERALS": "TRUE",
            "ENEMY_OFFICERS": "TRUE",
            "ENEMY_MEDICS_HEAL_SELF": "TRUE",
            "ENEMY_MEDICS": "TRUE",
            "ENEMYROLES": "TRUE",
        },
        "Tactical Interface Settings": {
            "PASSENGER_LEAVING_SWITCH_TO_NEW_SQUAD": "FALSE",
            "ADD_PASSENGER_TO_ANY_SQUAD": "TRUE",
        },
        "Tactical Gameplay Settings": {
            "ENEMIES_BLOW_OBSTACLES_UP": "FALSE",
            "ENEMIES_DONT_SPARE_LAUNCHABLES": "TRUE",
            "ENEMY_TANKS_ANY_PART_VISIBLE": "FALSE",
            "ENEMY_TANKS_BLOW_OBSTACLES_UP": "TRUE",
            "ENEMY_TANKS_DONT_SPARE_SHELLS": "TRUE",
            "ENEMY_TANKS_CAN_MOVE_IN_TACTICAL": "FALSE",
            "ALLOW_TANKS_DRIVING_OVER_PEOPLE": "TRUE",
            "ALLOW_CARS_DRIVING_OVER_PEOPLE": "TRUE",
            "ALLOW_DRIVING_VEHICLES_IN_TACTICAL": "TRUE",
            "USE_GLOBAL_BACKPACK_SETTINGS": "TRUE",
        },
    },
}


def set_ini_value(text: str, section: str, key: str, value: str) -> str:
    section_pattern = re.compile(
        rf"(?im)^\[{re.escape(section)}\][ \t]*\r?\n"
    )
    section_match = section_pattern.search(text)
    assignment = f"{key} = {value}"

    if section_match is None:
        suffix = "" if text.endswith(("\n", "\r")) else "\r\n"
        return f"{text}{suffix}\r\n[{section}]\r\n{assignment}\r\n"

    next_section = re.search(r"(?m)^\[[^\]\r\n]+\]", text[section_match.end() :])
    section_end = (
        section_match.end() + next_section.start()
        if next_section is not None
        else len(text)
    )
    section_text = text[section_match.end() : section_end]
    key_pattern = re.compile(rf"(?im)^[ \t]*{re.escape(key)}[ \t]*=.*$")

    if key_pattern.search(section_text):
        section_text = key_pattern.sub(assignment, section_text, count=1)
        return text[: section_match.end()] + section_text + text[section_end:]

    return text[:section_end] + assignment + "\r\n" + text[section_end:]


def patch_file(path: Path, sections: dict[str, dict[str, str]]) -> int:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        text = stream.read()
    count = 0
    for section, entries in sections.items():
        for key, value in entries.items():
            text = set_ini_value(text, section, key, value)
            count += 1
    with path.open("w", encoding="utf-8", newline="") as stream:
        stream.write(text)
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", type=Path, help="Data-1.13 directory")
    args = parser.parse_args()

    total = 0
    for filename, sections in SETTINGS.items():
        path = args.data_dir / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        updated = patch_file(path, sections)
        total += updated
        print(f"patched {path}: {updated} settings")
    print(f"total settings: {total}")


if __name__ == "__main__":
    main()
