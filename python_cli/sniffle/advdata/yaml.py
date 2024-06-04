# Written by Sultan Qasim Khan
# Copyright (c) 2024, NCC Group plc
# Released as open source under GPLv3

# Overly simplistic YAML parser for Bluetooth Assigned Numbers
# I made this to avoid adding a dependency
# This is not a general purpose parser
def decode_yaml(d: bytes):
    lines = d.split(b'\n')
    records = {}

    cur_record = None
    cur_name = None
    cur_subrecord = None

    for line in lines:
        if line.startswith(b'#') or len(line) == 0:
            continue
        elif line.startswith(b' '):
            ls = line.strip()
            if ls.startswith(b'-'):
                if cur_subrecord:
                    cur_record.append(cur_subrecord)
                cur_subrecord = {}
                ls = ls[2:]
            key, val = ls.split(b':')
            key_s = str(key.rstrip(), encoding='utf-8')
            val_s = str(val.lstrip(), encoding='utf-8')
            if val_s.startswith("0x"):
                val_s = int(val_s, 16)
            elif val_s.startswith("'"):
                val_s = val_s[1:-1]
            cur_subrecord[key_s] = val_s
        else:
            if cur_name:
                records[cur_name] = cur_record
            cur_name = str(line.strip()[:-1], encoding='utf-8')
            cur_record = []

    if cur_record:
        if cur_subrecord:
            cur_record.append(cur_subrecord)
        records[cur_name] = cur_record

    return records
