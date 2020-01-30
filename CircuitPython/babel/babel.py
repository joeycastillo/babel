import board
import displayio
import struct
try:
    from adafruit_bitmap_font import glyph_cache
    from babel.babelfont import BabelFont
except ImportError:
    glyph_cache = None

class AbstractBabel:
    """Abstract class for access to Unicode info / Unifont glyphs.
    Use FileBabel or FlashBabel depending on where you stored the Babel image."""
    BABEL_HEADER_EXTRA_TYPE_UPPERCASE_MAPPINGS = const(1)
    BABEL_HEADER_EXTRA_TYPE_LOWERCASE_MAPPINGS = const(2)
    BABEL_HEADER_EXTRA_TYPE_TITLECASE_MAPPINGS = const(3)
    BABEL_HEADER_EXTRA_TYPE_MIRRORING_MAPPINGS = const(4)

    def __init__(self):
        header = bytearray(20)
        self._read_address(4, header)
        (self.width,
         self.height,
         self.flags,
         self.last_codepoint,
         self.location_of_lut,
         self.location_of_glyphs,
         self.location_of_extras) = struct.unpack('<BBHIIII', header)

        mapping_info = bytearray(8)
        pos = self.location_of_extras
        while pos < self.location_of_lut:
            self._read_address(pos, mapping_info)
            pos = pos + 8
            (loc, len) = struct.unpack('<II', mapping_info)
            type = loc & 0xFF
            loc = loc >> 8
            flags = len & 0xFF
            len = len >> 8
            if type == BABEL_HEADER_EXTRA_TYPE_UPPERCASE_MAPPINGS:
                self.start_of_uppercase_mapping = loc
                self.end_of_uppercase_mapping = loc + len
            elif type == BABEL_HEADER_EXTRA_TYPE_LOWERCASE_MAPPINGS:
                self.start_of_lowercase_mapping = loc
                self.end_of_lowercase_mapping = loc + len
            elif type == BABEL_HEADER_EXTRA_TYPE_TITLECASE_MAPPINGS:
                self.start_of_titlecase_mapping = loc
                self.end_of_titlecase_mapping = loc + len
            elif type == BABEL_HEADER_EXTRA_TYPE_MIRRORING_MAPPINGS:
                self.start_of_mirrored_mapping = loc
                self.end_of_mirrored_mapping = loc + len

        self.info_for_replacement_character = self._fetch_glyph_basic_info(0xFFFD)
        self.extended_info_for_replacement_character = self._fetch_glyph_extended_info(0xFFFD)
        if glyph_cache is not None:
            self.font = BabelFont(self)
        else:
            self.font = None

    def _fetch_glyph_basic_info(self, codepoint):
        """Returns a packed 32-bit integer with basic information about the glyph.
        From LSB to MSB:
            * 21 bits: location of the glyph in the babel image
            * 5 bits : width of the glyph, should be <= 16
            * 2 bits : RTL nature
                        - 00: no RTL affinity
                        - 01: strong RTL affinity
                        - 10: strong LTR affinity
                        - 11: no RTL affinity, but mirrored when drawn in a RTL text run.
            * 1 bit  : is control character
            * 1 bit  : line break opportunity
        """
        loc = self.location_of_lut + codepoint * 6
        buf = bytearray(4)
        self._read_address(loc, buf)
        (retval,) = struct.unpack('<I', buf)

        return retval

    def _fetch_glyph_extended_info(self, codepoint):
        """Returns a packed 16-bit integer with basic information about the glyph.
        From LSB to MSB:
            * 5 bits : an enum of the character category, see babelconvert for details
            * 1 bit  : has uppercase mapping
            * 1 bit  : has lowercase mapping
            * 1 bit  : has titlecase mapping
            * 4 bits : an enum of the bidi class, see babelconvert for details
            * 1 bit  : is whitespace
        The two high bits are unset and may be used for features in the future.
        """
        loc = 4 + self.location_of_lut + codepoint * 6
        buf = bytearray(2)
        self._read_address(loc, buf)
        (retval,) = struct.unpack('<H', buf)

        return retval

    def _search_mapping(self, start, first, last, key):
        retval = None
        if first > last:
            return retval
        mid = int((first + last) / 2)
        buf = bytearray(4)
        self._read_address(start + mid * 4, buf)
        (testkey,testvalue) = struct.unpack('<HH', buf)
        if key == testkey:
            retval = mid
        else:
            if key < testkey:
                retval = self._search_mapping(start, first, mid - 1, key)
            else:
                retval = self._search_mapping(start, mid + 1, last, key)
        return retval

    def _mapping_for_codepoint(self, codepoint, start, end):
        """Searches a mapping table (i.e. lowercase -> UPPERCASE) for a glyph.
        If no mapping exists, returns the original value. Relatively expensive to call;
        first check the extended info flags to make sure a mapping exists."""
        last_index = int((end - start) / 4)
        index_of_result = self._search_mapping(start, 0, last_index, codepoint)
        if index_of_result is not None:
            buf = bytearray(4)
            self._read_address(start + index_of_result * 4, buf)
            (_, retval) = struct.unpack('<HH', buf)
            return retval
        else:
            return codepoint

    def _uppercase_mapping_for_codepoint(self, codepoint):
        return self._mapping_for_codepoint(codepoint, self.start_of_uppercase_mapping, self.end_of_uppercase_mapping)

    def _lowercase_mapping_for_codepoint(self, codepoint):
        return self._mapping_for_codepoint(codepoint, self.start_of_lowercase_mapping, self.end_of_lowercase_mapping)

    def localized_uppercase(self, string):
        """Returns an uppercase version of the string passed in."""
        retval = ""
        for c in string:
            info = self._fetch_glyph_extended_info(ord(c))
            if info & 0x20 == 0: # this bit indicates whether an uppercase mapping exists
                retval += c
            else:
                retval += chr(self._uppercase_mapping_for_codepoint(ord(c)))

        return retval

    def localized_lowercase(self, string):
        """Returns a lowercase version of the string passed in."""
        retval = ""
        for c in string:
            info = self._fetch_glyph_extended_info(ord(c))
            if info & 0x40 == 0: # this bit indicates whether a lowercase mapping exists
                retval += c
            else:
                retval += chr(self._lowercase_mapping_for_codepoint(ord(c)))

        return retval

class FileBabel(AbstractBabel):
    def __init__(self, filename = 'BABEL.BIN'):
        self.file = open(filename, 'rb')
        super().__init__()

    def _read_address(self, address, read_buffer):
        self.file.seek(address)
        self.file.readinto(read_buffer)
        return read_buffer

class FlashBabel(AbstractBabel):
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
