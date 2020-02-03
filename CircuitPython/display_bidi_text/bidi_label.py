"""
Simple subclass of adafruit_display_text's Label; overrides the _update_text method to provide
minimally viable bidirectional layout support. Treats x as the origin, so LTR text will start at x
and make its way to the right, and RTL text will start at x and make its way to the left. Ideally 
this should have a width property so it can reset to a right margin for RTL text runs, and a left
margin for LTR text runs. For now, set x to 0 for displaying LTR text and set it to a nonzero value
(like your display's width or width / 2) for RTL.

Also note: instead of allowing inline direction changes, direction changes cause a newline, i.e. 
a RTL text run inside of a LTR text run will trigger line breaks so each run can appear on its
own line.
"""
import displayio
from adafruit_display_text import label

class BidiLabel(label.Label):
    def _update_text(self, new_text): # pylint: disable=too-many-locals
        x = 0
        y = 0
        i = 0
        direction = 1
        old_c = 0
        y_offset = int((self.font.get_glyph(ord('M')).height -
                        new_text.count('\n') * self.height * self.line_spacing) / 2)
        #print("y offset from baseline", y_offset)
        top = bottom = left = right = 0
        for character in new_text:
            if character == '\n':
                y += int(self.height * self._line_spacing)
                x = 0
                continue
            glyph = self.font.get_glyph(ord(character))
            if not glyph:
                continue
            if direction == -1 and glyph.mirrored:
                glyph = self.font.get_glyph(glyph.mirrored)
            if glyph.rtl and direction == 1:
                if x != 0:
                    y += int(self.height * self._line_spacing)
                    x = 0
                direction = -1
            elif glyph.ltr and direction == -1:
                if x != 0:
                    y += int(self.height * self._line_spacing)
                    x = 0
                direction = 1
            right = max(right, x+glyph.width*direction)
            if y == 0:   # first line, find the Ascender height
                top = min(top, -glyph.height+y_offset)
            bottom = max(bottom, y-glyph.dy+y_offset)
            position_y = y - glyph.height - glyph.dy + y_offset
            position_x = x + glyph.dx * direction
            if not self._text or old_c >= len(self._text) or character != self._text[old_c]:
                try:
                    face = displayio.TileGrid(glyph.bitmap, pixel_shader=self.palette,
                                              default_tile=glyph.tile_index,
                                              tile_width=glyph.width, tile_height=glyph.height,
                                              position=(position_x, position_y))
                except TypeError:
                    face = displayio.TileGrid(glyph.bitmap, pixel_shader=self.palette,
                                              default_tile=glyph.tile_index,
                                              tile_width=glyph.width, tile_height=glyph.height,
                                              x=position_x, y=position_y)
                if i < len(self):
                    self[i] = face
                else:
                    self.append(face)
            elif self._text and character == self._text[old_c]:
                try:
                    self[i].position = (position_x, position_y)
                except AttributeError:
                    self[i].x = position_x
                    self[i].y = position_y

            x += glyph.shift_x * direction

            # TODO skip this for control sequences or non-printables.
            i += 1
            old_c += 1
            # skip all non-prinables in the old string
            while (self._text and old_c < len(self._text) and
                   (self._text[old_c] == '\n' or not self.font.get_glyph(ord(self._text[old_c])))):
                old_c += 1
        # Remove the rest
        while len(self) > i:
            self.pop()
        self._text = new_text
        self._boundingbox = (left, top, left+right, bottom-top)
