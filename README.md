# Babel Universal Language Library

Building on the ideas [I was exploring over here](https://github.com/joeycastillo/Adafruit-GFX-Library). The gist: rather than muck about looking for glyph data in a file on a filesystem, just dedicate an entire 2 MB chip to nothing but universal language support. You end up saving on storage space and on RAM, and it's simple: you just point the chip at an address and get the bits as fast as your bus can clock them in.

The goal remains the same: performant display of all the languages of the world.

## Background

The [GD25Q16C SPI Flash chip](https://www.digikey.com/product-detail/en/GD25Q16CTIGR/1970-1010-1-ND/9484760/) can hold 2,097,152 bytes. Squashing everything I put into the GFX fork — bitmaps, width, basic bidirectional info and spacing — got me to 1,923,376 bytes, leaving about 170 KB to play with. So I added: 

* Two more bytes per character for additional metadata, including [general category](https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)) and proper [bidi class](https://en.wikipedia.org/wiki/Template:Bidi_Class_(Unicode)), for more technically correct bidirectional algorithm implementation
* A bit to indicate whether the character is [whitespace](https://www.unicode.org/Public/UCD/latest/ucd/PropList.txt).
* A bit to indicate [word wrapping opportunities](https://www.unicode.org/Public/UCD/latest/ucd/LineBreak.txt).
* One-to-one case mappings from uppercase to lowercase and lowercase to uppercase / titlecase for all bicameral scripts in the Basic Multilingual Plane.
* Mappings of supported BMP glyphs to their mirror images, for correct [bidirectional mirroring](https://www.unicode.org/Public/UCD/latest/ucd/BidiMirroring.txt) in right-to-left text runs.
* A lookup table for mapping isolated Perso-Arabic characters to connected presentation forms.

This still leaves just over 25 kilobytes at the end, for more mappings or other glyph-specific features. There are also two free bits per character in the additional metadata field, for general features that apply to all glyphs. Haven't decided how to use them yet.

As of February 2020 I'm considering a return to the filesystem use case, for a couple of reasons: one, most of the devices I want to use this with already have a Flash chip; making it bigger is cheaper than adding a second one. It also frees up a microcontroller pin. Mostly though it opens up the possibility of supporting more Unicode planes; without the 2MB limitation, we can add even more glyphs!

## Project Structure

* `babelconvert` - a hastily assembled python script to generate the Flash image.
* `src` - an Arduino library that allows basic access to the glyph data and metadata. Very work-in-progress.
* `BabelTest` and `BabelTest.xcodeproj` - Uses the same base class from `src` but implements a mock version using a file on the file system. Good for testing.
* `examples` - Arduino sketches: 
  - `BurnBabelBurn` burns the Babel image to a chip. 
  - `BabelView` dumps all character info to Serial. 
* `sample.txt` - output of the `BabelTest` tool, previews of all glyphs plus what the babel.bin metadata says about them.

## Next Steps

- [X] Create a subclass of Babel that can draw text to a GFX display.
  - [X] Handle screen size and margins, clipping
  - [ ] Handle character wrapping
  - [X] Handle RTL direction changes
  - [X] Handle combining marks
  - [X] Glyph magnification (i.e. size=2)
- [ ] String manipulation
  - [X] Uppercase
  - [X] Lowercase
  - [ ] Capitalization
  - [ ] Word wrap (WIP)
- [X] Make a [simple FeatherWing with the chip](https://github.com/joeycastillo/Feather-Projects/tree/master/Experiments), for easier testing on more devices. 
- [ ] [Port to CircuitPython!](https://github.com/joeycastillo/babel/tree/master/CircuitPython/babel)
