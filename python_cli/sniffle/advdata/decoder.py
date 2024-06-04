# Written by Sultan Qasim Khan
# Copyright (c) 2024, NCC Group plc
# Released as open source under GPLv3

from struct import unpack
from .constants import ad_types

class AdvDataRecord:
    def __init__(self, data_type: int, data: bytes):
        self.type = data_type
        self.data = data

    def str_type(self):
        if self.type in ad_types:
            return ad_types[self.type]
        else:
            return "Unknown Advertising Data Type: 0x%02X" % self.type

    def __str__(self):
        return "%s\n    Length: %d\n    Value: %s" % (
                self.str_type(), len(self.data), repr(self.data))

class FlagsRecord(AdvDataRecord):
    def __str__(self):
        if len(self.data) == 1:
            return "%s: 0x%02X" % (self.str_type(), self.data[0])
        else:
            return "%s: Malformed" % self.str_type()

class ServiceList16Record(AdvDataRecord):
    pass

class ServiceList32Record(AdvDataRecord):
    pass

class ServiceList128Record(AdvDataRecord):
    pass

class LocalNameRecord(AdvDataRecord):
    def __str__(self):
        try:
            name = str(self.data, encoding='utf-8')
        except:
            name = repr(self.data) + " (Invalid UTF-8)"
        return "%s: %s" % (self.str_type(), name)

class ShortenedLocalNameRecord(LocalNameRecord):
    pass

class CompleteLocalNameRecord(LocalNameRecord):
    pass

class TXPowerLevelRecord(AdvDataRecord):
    def __str__(self):
        if len(self.data) == 1:
            power, = unpack('<b', self.data)
            return "%s: %d dBm" % (self.str_type(), power)
        else:
            return "%s: Malformed" % self.str_type()

class ServiceData16Record(AdvDataRecord):
    pass

class ServiceData32Record(AdvDataRecord):
    pass

class ServiceData128Record(AdvDataRecord):
    pass

class ManufacturerSpecificDataRecord(AdvDataRecord):
    pass

# https://bitbucket.org/bluetooth-SIG/public/src/main/assigned_numbers/core/ad_types.yaml
ad_type_classes = {
    0x01: FlagsRecord,
    0x03: ServiceList16Record,
    0x05: ServiceList32Record,
    0x07: ServiceList128Record,
    0x08: ShortenedLocalNameRecord,
    0x09: CompleteLocalNameRecord,
    0x0A: TXPowerLevelRecord,
    0x16: ServiceData16Record,
    0x20: ServiceData32Record,
    0x21: ServiceData128Record,
    0xFF: ManufacturerSpecificDataRecord
}

def record_from_type_data(data_type: int, data: bytes):
    if data_type in ad_type_classes:
        return ad_type_classes[data_type](data_type, data)
    else:
        return AdvDataRecord(data_type, data)

def decode_adv_data(data):
    records = []
    i = 0

    while i < len(data):
        try:
            l = data[i]
            t = data[i+1]
            d = data[i+2:i+1+l]
            records.append(record_from_type_data(t, d))
            i += 1+l
        except:
            break

    return records
