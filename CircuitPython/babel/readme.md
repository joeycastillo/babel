# Babel for CircuitPython

WIP, currently supports Babel on a dedicated flash chip and as a file on a CircuitPython file system.

Features: 

* [Adafruit_CircuitPython_Bitmap_Font](https://github.com/adafruit/Adafruit_CircuitPython_Bitmap_Font)-compatible bitmap font.
* Localized case mapping to upper and lower case for the Basic Multilingual Plane

## Examples

With a file on the filesystem:

```import board
from babel.babel import Babel
from adafruit_display_text import label

babel = Babel() # assumes BABEL.BIN or pass in a filename
display = board.DISPLAY
text = """Short sayings:
जान है तो जहान है
風向轉變時,有人築牆,\n有人造風車
Один в поле не воин.
ἄνθρωπος μέτρον
"""
uppercase_text = babel.localized_uppercase(text)

text_area = label.Label(babel.font, text=uppercase_text, color=0xFFFFFF)
text_area.x = 0
text_area.y = 72
display.show(text_area)

while True:
    pass
```

With a dedicated Flash chip for Babel:

```import board
import digitalio
from babel.babel import FlashBabel
from adafruit_display_text import label

cs = digitalio.DigitalInOut(board.D6)
babel = FlashBabel(cs)

display = board.DISPLAY
text = """Short sayings:
जान है तो जहान है
風向轉變時,有人築牆,\n有人造風車
Один в поле не воин.
ἄνθρωπος μέτρον
"""
uppercase_text = babel.localized_uppercase(text)

text_area = label.Label(babel.font, text=uppercase_text, color=0xFFFFFF)
text_area.x = 0
text_area.y = 72
display.show(text_area)

while True:
    pass
```