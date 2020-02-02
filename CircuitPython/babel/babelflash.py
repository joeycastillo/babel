import board
from babel.babel import _Babel

class FlashBabel(_Babel):
    SFLASH_CMD_READ = const(0x03)
    SFLASH_CMD_READ_STATUS = const(0x05)
    SFLASH_CMD_READ_STATUS2 = const(0x35)
    SFLASH_CMD_ENABLE_RESET = const(0x66)
    SFLASH_CMD_RESET = const(0x99)
    SFLASH_CMD_WRITE_DISABLE = const(0x04)

    def __init__(self, spi_cs, spi_bus = board.SPI()):
        from adafruit_bus_device.spi_device import SPIDevice as spidev
        _spi = spidev(spi_bus, spi_cs, baudrate=1000000)

        read_buffer = bytearray(1)
        # We don't know what state the flash is in, so make sure it's not up to anything, then reset.
        with _spi as spi:
            while True:
                # The write in progress bit should be low.
                spi.write(bytearray([SFLASH_CMD_READ_STATUS]))
                spi.readinto(read_buffer)
                if read_buffer[0] & 0x01 == 0:
                    break
            while True:
                # The suspended write/erase bit should be low.
                spi.write(bytearray([SFLASH_CMD_READ_STATUS2]))
                spi.readinto(read_buffer)
                if read_buffer[0] & 0x80 == 0:
                    break
            # reset and disable writes
            spi.write(bytearray([SFLASH_CMD_ENABLE_RESET]))
            spi.write(bytearray([SFLASH_CMD_RESET]))
            spi.write(bytearray([SFLASH_CMD_WRITE_DISABLE]))
        self._spi = _spi
        super().__init__()

    def _read_address(self, address, read_buffer):
        write_buffer = bytearray(4)
        write_buffer[0] = SFLASH_CMD_READ
        write_buffer[1] = (address >> 16) & 0xFF
        write_buffer[2] = (address >> 8) & 0xFF
        write_buffer[3] = address & 0xFF
        with self._spi as spi:
            spi.write(write_buffer)
            spi.readinto(read_buffer)
        return read_buffer
