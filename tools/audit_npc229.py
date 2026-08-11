#!/usr/bin/env python3
import struct
from pathlib import Path

path = Path('Patch/Data-1.13/NpcData/229.EDT')
data = path.read_bytes()
record_bytes = 480
assert len(data) % record_bytes == 0
for index, offset in enumerate(range(0, len(data), record_bytes), 1):
    raw = data[offset:offset + record_bytes]
    values = struct.unpack('<' + 'H' * (len(raw) // 2), raw)
    chars = []
    for value in values:
        if value == 0:
            break
        if value > 33:
            value -= 1
        chars.append(chr(value))
    text = ''.join(chars)
    if text.strip():
        print(f'{index}\t0x{offset:08X}\t{text}')
