import displayio
from adafruit_bitmap_font import glyph_cache
from display_bidi_text import bidi_glyph

class BabelFont(glyph_cache.GlyphCache):
    def __init__(self, babel):
        self.babel = babel
        super().__init__()

    def get_bounding_box(self):
        # max width is double the normal width (16x16)
        return (self.babel.width * 2, self.babel.height, 0, 0)

    def load_glyphs(self, code_points):
        if isinstance(code_points, int):
            remaining = set()
            remaining.add(code_points)
        elif isinstance(code_points, str):
            remaining = set(ord(c) for c in code_points)
        elif isinstance(code_points, set):
            remaining = code_points
        else:
            remaining = set(code_points)
        for code_point in remaining:
            if code_point in self._glyphs and self._glyphs[code_point]:
                remaining.remove(code_point)
        if not remaining:
            return
        while remaining:
            codepoint = remaining.pop()
            info = None
            if codepoint <= self.babel.last_codepoint:
                info = self.babel._fetch_glyph_basic_info(codepoint)
            if info is None or info == 0:
                # info can be None if asking for a glyph > 0xFFFF
                # info can be 0 if asking for an invalid glyph <= 0xFFFF
                # either way, give them the replacement character
                info = self.babel.info_for_replacement_character
            loc = info & 0x3FFFFF
            width = (info >> 22) & 0x1F
            bitmap = displayio.Bitmap(width, self.babel.height, 2)
            if width > 8:
                buf = bytearray(32)
                self.babel._read_address(loc, buf)
                for y in range(len(buf) / 2):
                    for side in range(2):
                        for x in range(8):
                            bit = (buf[2 * y + side] >> (7 - x)) & 1
                            bitmap[x + 8 * side, y] = bit
            else:
                buf = bytearray(16)
                self.babel._read_address(loc, buf)
                for y in range(len(buf)):
                    for x in range(8):
                        bit = (buf[y] >> (7 - x)) & 1
                        bitmap[x, y] = bit
            nsm = (info & 0x8000000) != 0
            mirrored = None
            if (info & 0x30000000) == 0x30000000:
                mirrored = self.babel.mirrored_mapping_for_codepoint(code_point)
            rtl = False if mirrored else (info & 0x10000000) != 0
            ltr = False if mirrored else (info & 0x20000000) != 0
            self._glyphs[code_point] = bidi_glyph.BidiGlyph(bitmap, 0, width, self.babel.height, -width if nsm else 0, 0, 0 if nsm else width, 0, rtl, ltr, mirrored)