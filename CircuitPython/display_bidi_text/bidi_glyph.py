class BidiGlyph:
    def __init__(self, bitmap, tile_index, width, height, dx, dy, shift_x, shift_y, rtl, ltr, mirrored = None):
        self.bitmap = bitmap
        self.tile_index = tile_index
        self.width = width
        self.height = height
        self.dx = dx
        self.dy = dy
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.rtl = rtl
        self.ltr = ltr
        self.mirrored = mirrored
