import displayio
import struct
from adafruit_bitmap_font import glyph_cache
from babel.babelfont import BabelFont

class _PlaneInfo:
    def __init__(self, first, last, lut):
        self.first_codepoint = first
        self.last_codepoint = last
        self.location_of_lut = lut

class _Babel:
    """Abstract class for access to Unicode info / Unifont glyphs.
    Use FileBabel or FlashBabel depending on where you stored the Babel image."""
    BABEL_HEADER_EXTRA_TYPE_UPPERCASE_MAPPINGS = const(1)
    BABEL_HEADER_EXTRA_TYPE_LOWERCASE_MAPPINGS = const(2)
    BABEL_HEADER_EXTRA_TYPE_TITLECASE_MAPPINGS = const(3)
    BABEL_HEADER_EXTRA_TYPE_MIRRORING_MAPPINGS = const(4)
    BABEL_HEADER_EXTRA_TYPE_ARABIC_MAPPINGS = const(64)

    def __init__(self):
        header = bytearray(32)
        self._read_address(4, header)
        (self.width,
         self.height,
         self.flags,
         self.location_of_glyphs,
         first_plane0_codepoint,
         last_plane0_codepoint,
         location_of_plane0_lut,
         first_plane1_codepoint,
         last_plane1_codepoint,
         location_of_plane1_lut,
         first_plane2_codepoint,
         last_plane2_codepoint,
         location_of_plane2_lut) = struct.unpack('<BBHIHHIHHIHHI', header)
        self.planes = [_PlaneInfo(first_plane0_codepoint, last_plane0_codepoint, location_of_plane0_lut),
                       _PlaneInfo(first_plane1_codepoint, last_plane1_codepoint, location_of_plane1_lut),
                       _PlaneInfo(first_plane2_codepoint, last_plane2_codepoint, location_of_plane2_lut)]
        extras = bytearray(4)
        self._read_address(148, extras)
        self.location_of_extras = struct.unpack('<I', extras)[0]

        mapping_info = bytearray(8)
        pos = self.location_of_extras
        while pos < location_of_plane0_lut:
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
            elif type == BABEL_HEADER_EXTRA_TYPE_ARABIC_MAPPINGS:
                self.start_of_arabic_mapping = loc
                self.arabic_mapping_num_entries = int(len // (2 * 4)) # 4 entries of 2 bytes each

        replacement_character = 0xFFFD if last_plane0_codepoint >= 0xFFFD else 0x003F # question mark
        self.info_for_replacement_character = self._fetch_glyph_basic_info(replacement_character)
        self.extended_info_for_replacement_character = self._fetch_glyph_extended_info(replacement_character)
        if glyph_cache is not None:
            self.font = BabelFont(self)
        else:
            self.font = None

    def _fetch_glyph_basic_info(self, codepoint):
        """Returns a packed 32-bit integer with basic information about the glyph.
        From LSB to MSB:
            * 22 bits: location of the glyph in the babel image
            * 5 bits : width of the glyph, should be <= 16
            * 1 bit  : is nonspacing mark
            * 2 bits : RTL nature
                        - 00: no RTL affinity
                        - 01: strong RTL affinity
                        - 10: strong LTR affinity
                        - 11: no RTL affinity, but mirrored when drawn in a RTL text run.
            * 1 bit  : is control character
            * 1 bit  : line break opportunity
        """
        plane = None
        location_in_plane = codepoint & 0xFFFF
        try:
            plane = self.planes[codepoint >> 16]
            if codepoint >> 16:
                print(codepoint >> 16, plane, codepoint, plane.first_codepoint, plane.last_codepoint)
            if location_in_plane > plane.last_codepoint or location_in_plane < plane.first_codepoint:
                raise IndexError()
        except IndexError:
            return self.info_for_replacement_character
        loc = plane.location_of_lut + ((codepoint - plane.first_codepoint) & 0xFFFF) * 6
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
            * 1 bit  : has bidi mirroring mapping
            * 1 bit  : is whitespace
        The two high bits are unset and may be used for additional features in the future.
        """
        plane = None
        location_in_plane = codepoint & 0xFFFF
        try:
            plane = self.planes[codepoint >> 16]
            if location_in_plane > plane.last_codepoint or codepoint < plane.first_codepoint:
                raise IndexError()
        except IndexError:
            return self.extended_info_for_replacement_character
        loc = 4 + plane.location_of_lut + ((codepoint - plane.first_codepoint) & 0xFFFF) * 6
        buf = bytearray(2)
        self._read_address(loc, buf)
        (retval,) = struct.unpack('<H', buf)

        return retval

    def _search_mapping(self, codepoint, address, last, first = 0):
        """Performs a binary search on one of the mapping tables. Parameters:
        codepoint: the codepoint you're searching for
        address: the address in babel.bin where the mapping table resides
        last: last index that should be considered (i.e. len - 1)
        first: first index that should be considered (omit; should be 0 until we start searching)
        Returns an index into the mapping table where the codepoint was found,
        or None if the codepoint was not found."""
        retval = None
        if first > last:
            return retval
        mid = int((first + last) / 2)
        buf = bytearray(4)
        self._read_address(address + mid * 4, buf)
        (key,value) = struct.unpack('<HH', buf)
        if codepoint == key:
            retval = mid
        else:
            if codepoint < key:
                retval = self._search_mapping(codepoint, address, mid - 1, first)
            else:
                retval = self._search_mapping(codepoint, address, last, mid + 1)
        return retval

    def _mapping_for_codepoint(self, codepoint, start, end):
        """Searches a mapping table (i.e. lowercase -> UPPERCASE) for a glyph.
        If no mapping exists, returns the original value.
        Relatively expensive to call; O(log(n)) based on the size of the mapping table;
        before calling, check the extended info flags to make sure a mapping exists."""
        last_index = int((end - start) / 4)
        index_of_result = self._search_mapping(codepoint, start, last_index)
        if index_of_result is not None:
            buf = bytearray(4)
            self._read_address(start + index_of_result * 4, buf)
            (_, retval) = struct.unpack('<HH', buf)
            return retval
        else:
            return codepoint

    def _uppercase_mapping_for_codepoint(self, codepoint):
        """Returns an uppercase version of the codepoint passed in,
        or the same codepoint if there is no uppercase mapping table available."""
        try:
            return self._mapping_for_codepoint(codepoint, self.start_of_uppercase_mapping, self.end_of_uppercase_mapping)
        except AttributeError:
            return codepoint

    def _lowercase_mapping_for_codepoint(self, codepoint):
        """Returns a lowercase version of the codepoint passed in,
        or the same codepoint if there is no lowercase mapping table available."""
        try:
            return self._mapping_for_codepoint(codepoint, self.start_of_lowercase_mapping, self.end_of_lowercase_mapping)
        except AttributeError:
            return codepoint

    def mirrored_mapping_for_codepoint(self, codepoint):
        """Returns the mirror image of this glyph for use in right-to-left text runs,
        or the same codepoint if there is no mirror mapping table available."""
        try:
            return self._mapping_for_codepoint(codepoint, self.start_of_mirrored_mapping, self.end_of_mirrored_mapping)
        except AttributeError:
            return codepoint

    def _arabic_mapping_for_codepoint(self, codepoint):
        """Returns an array of length 4, containing up to four alternate glyph forms for a
        given codepoint in the order: isolated, initial, medial, final. Forms that do not
        exist (i.e. a medial Alef) are set to 0. If the codepoint has no alternate glyph
        forms, returns None. See notes in babelconvert for more details about Arabic
        shaping and this lookup table."""
        index = codepoint - 0x0621
        if index < 0 or index > self.arabic_mapping_num_entries:
            return None
        buf = bytearray(8)
        self._read_address(self.start_of_arabic_mapping + 8 * index, buf)
        if buf[0] == 0:
            # all characters that support shaping have an isolated form.
            # if this entry doesn't, it's not a valid entry.
            return None
        else:
            return list(struct.unpack('<4H', buf))

    def localized_uppercase(self, string):
        """Returns an uppercase version of the string passed in, or the same string if
        there is no uppercase mapping table available."""
        retval = ""
        for c in string:
            info = self._fetch_glyph_extended_info(ord(c))
            if info & 0x20 == 0: # this bit indicates whether an uppercase mapping exists
                retval += c
            else:
                retval += chr(self._uppercase_mapping_for_codepoint(ord(c)))

        return retval

    def localized_lowercase(self, string):
        """Returns a lowercase version of the string passed in, or the same string if
        there is no lowercase mapping table available."""
        retval = ""
        for c in string:
            info = self._fetch_glyph_extended_info(ord(c))
            if info & 0x40 == 0: # this bit indicates whether a lowercase mapping exists
                retval += c
            else:
                retval += chr(self._lowercase_mapping_for_codepoint(ord(c)))

        return retval

    FORM_ISOLATED = const(0)
    FORM_INITIAL = const(1)
    FORM_MEDIAL = const(2)
    FORM_FINAL = const(3)

    def shape_arabic(self, string):
        """Returns a version of the input string that maps Arabic characters to shaped forms.
           If Arabic shaping information is unavailable, returns the original string.
           See babelconvert for a primer on Arabic shaping and this algorithm."""
        if not hasattr(self, 'start_of_arabic_mapping'):
            return string

        retval = ""
        for i in range(0, len(string)):
            current_codepoint = ord(string[i])
            if current_codepoint >> 8 != 0x06:
                # we only need to check the Arabic block
                retval += chr(current_codepoint)
                continue

            forms = self._arabic_mapping_for_codepoint(current_codepoint)
            if forms is None:
                # this character does not have shaping information (numerals, diacritics, etc.)
                retval += chr(current_codepoint)
            else:
                # determine if there is a previous character to connect to or end on
                previous_index = i - 1
                while previous_index >= 0:
                    candidate = ord(string[previous_index])
                    info = self._fetch_glyph_basic_info(candidate)
                    # this looks confusing but the conditional is basically:
                    #   is the candidate character in the Arabic block?
                    #   is the candidate character a non-spacing mark?
                    # if both are true, don't stop, keep looking.
                    if not (candidate >> 8 == 0x06 and info & 0x8000000 != 0):
                        break
                    previous_index -= 1
                # if we're at the beginning of the string, clearly there's nothing to connect to.
                previous = None if previous_index < 0 else ord(string[previous_index])
                if previous is not None:
                    previous_forms = self._arabic_mapping_for_codepoint(previous)
                    if previous_forms is None or (previous_forms[FORM_INITIAL] == 0 and previous_forms[FORM_MEDIAL] == 0):
                        # also if the previous character has no way to connect to us.
                        previous = None

                # now determine if there is a next character to connect to or end on
                next_index = i + 1
                while next_index < len(string):
                    candidate = ord(string[next_index])
                    info = self._fetch_glyph_basic_info(candidate)
                    if not (candidate >> 8 == 0x06 and info & 0x8000000 != 0):
                        # see above for notes on this conditional
                        break
                    next_index += 1
                # again, at the end, nothing to connect to
                next = None if next_index >= len(string) else ord(string[next_index])
                if next is not None:
                    next_forms = self._arabic_mapping_for_codepoint(next)
                    if next_forms is None or (next_forms[FORM_MEDIAL] == 0 and next_forms[FORM_FINAL] == 0):
                        # the next character has to have a medial or final form for us to connect to it.
                        next = None

                # handle one special case: if current is Lam and next is Alef, we need a Lam-Alef ligature.
                if current_codepoint == 0x0644 and next in [0x0622, 0x0623, 0x0625, 0x0627]:
                    if next == 0x0622:
                        retval += chr(0xFEF5) if previous is None else chr(0xFEF6)
                    if next == 0x0623:
                        retval += chr(0xFEF7) if previous is None else chr(0xFEF8)
                    if next == 0x0625:
                        retval += chr(0xFEF9) if previous is None else chr(0xFEFA)
                    if next == 0x0627:
                        retval += chr(0xFEFB) if previous is None else chr(0xFEFC)
                    continue

                # from here it's pretty straightforward: we know what comes before and what comes after,
                # and the forms array contains the forms we support.
                if previous is not None and next is not None and forms[FORM_MEDIAL] > 0:
                    retval += chr(forms[FORM_MEDIAL])
                elif next is not None and forms[FORM_INITIAL] > 0:
                    retval += chr(forms[FORM_INITIAL])
                elif previous is not None and forms[FORM_FINAL] > 0:
                    retval += chr(forms[FORM_FINAL])
                else:
                    retval += chr(forms[FORM_ISOLATED])
        return retval

class Babel(_Babel):
    def __init__(self, filename = 'BABEL.BIN'):
        self.file = open(filename, 'rb')
        super().__init__()

    def _read_address(self, address, read_buffer):
        self.file.seek(address)
        self.file.readinto(read_buffer)
        return read_buffer
