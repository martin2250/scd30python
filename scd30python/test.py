#!/usr/bin/python
import struct

# regs = [0x43DB, 0x8c2e, 0x41d9, 0xe7ff, 0x4243, 0x3a1b]
# regs_bin = struct.pack('>6H', *regs)
# print(struct.unpack('>3f', regs_bin))

import scd30


sensor = scd30.SCD30('/dev/ttyUSB0')

print(sensor.read())