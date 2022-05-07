import minimalmodbus
import struct


class SCD30:
    """SCD 30"""
    def __init__(self, path: str):
        self.mod = minimalmodbus.Instrument(path, 0x61)

    def start_continuous(self, pressure: int = 0x0000):
        if pressure not in range(0, 0x10000):
            raise ValueError('pressure out of range')
        self.mod.write_register(0x0036, pressure, functioncode=6)

    @property
    def measurement_interval(self) -> int:
        return self.mod.read_register(0x0025)

    @measurement_interval.setter
    def measurement_interval(self, interval: int):
        if interval not in range(2, 1801):
            raise ValueError('interval out of range')
        self.mod.write_register(0x0025, interval, functioncode=6)

    @property
    def enable_asc(self) -> bool:
        return bool(self.mod.read_register(0x003a))

    @enable_asc.setter
    def enable_asc(self, enable: bool):
        self.mod.write_register(0x003a, int(enable), functioncode=6)

    @property
    def temperature_offset(self) -> float:
        return self.mod.read_register(0x003b, 2)

    @temperature_offset.setter
    def temperature_offset(self, offset: float):
        self.mod.write_register(0x003b, offset, 2, functioncode=6)

    def get_firmware_version(self) -> int:
        return self.mod.read_register(0x0020)

    def force_cal(self, reference: int):
        if reference not in range(400, 2001):
            raise ValueError('co2 reference value out of range')
        self.mod.write_register(0x0039, reference, functioncode=6)

    def soft_reset(self):
        self.mod.write_register(0x0034, 0x0001, functioncode=6)

    @enable_asc.setter
    def enable_asc(self, enable: bool):
        self.mod.write_register(0x003a, int(enable), functioncode=6)

    def get_ready(self) -> bool:
        return bool(self.mod.read_register(0x0027))

    def read(self):
        regs = self.mod.read_registers(0x0028, 6)
        regs_bin = struct.pack('>6H', *regs)
        return struct.unpack('>3f', regs_bin)
