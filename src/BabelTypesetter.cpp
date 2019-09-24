/*
 * The MIT License (MIT)
 *
 * Copyright © 2019 Joey Castillo. All rights reserved.
 * Incorporates ideas and code from the Adafruit_GFX library.
 * Copyright (c) 2013 Adafruit Industries.  All rights reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <string.h>
#include <stdlib.h>
#include "BabelTypesetter.h"

#ifndef _swap_int16_t
#define _swap_int16_t(a, b) { int16_t t = a; a = b; b = t; }
#endif

BabelTypesetter::BabelTypesetter() {
}

void BabelTypesetter::begin() {
    this->glyphStorage->begin();
}

void BabelTypesetter::setCursor(int16_t x, int16_t y) {
    this->cursor_x = x;
    this->cursor_y = y;
}

void BabelTypesetter::drawFillRect(int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color) {
    for (int16_t i=x; i<x+w; i++) {
        for (int16_t j=y; j<y+h; j++) {
            this->drawPixel(x, y, color);
        }
    }
}

int BabelTypesetter::drawGlyph(int16_t x, int16_t y, BabelGlyph glyph, uint16_t color) {
    uint8_t width = BABEL_INFO_GET_GLYPH_WIDTH(glyph.info);
    uint8_t characterWidth = width > 8 ? 2 : 1; // <=8x16 glyphs fit in 16 bytes. >8x16 require two.
    bool mirrored = ((1 == -1) && BABEL_INFO_GET_MIRRORED_IN_RTL(glyph.info));

    if (mirrored) {
        switch (characterWidth) {
            case 1:
                for(int8_t i=0; i<characterWidth*16; i++ ) {
                    uint8_t line = glyph.glyphData[i];
                    for(int8_t j=7; j>= 0; j--, line >>= 1) {
                        if(line & 1) {
                            drawPixel(x+8-j, y+i, color);
                        }
                    }
                }
                break;
            case 2:
                for(int8_t i=0; i<characterWidth*16; i++ ) {
                    uint8_t line = glyph.glyphData[i];
                    for(int8_t j=7; j>= 0; j--, line >>= 1) {
                        if(line & 1) {
                            drawPixel(x+8-(j+(i%2?8:0)), y+i/2, color);
                        }
                    }
                }
                break;
        }
    } else {
        switch (characterWidth) {
            case 1:
                for(int8_t i=0; i<characterWidth*16; i++ ) {
                    uint8_t line = glyph.glyphData[i];
                    for(int8_t j=7; j>= 0; j--, line >>= 1) {
                        if(line & 1) {
                            drawPixel(x+j, y+i, color);
                        }
                    }
                }
                break;
            case 2:
                for(int8_t i=0; i<characterWidth*16; i++ ) {
                    uint8_t line = glyph.glyphData[i];
                    for(int8_t j=7; j>= 0; j--, line >>= 1) {
                        if(line & 1) {
                            drawPixel(x+j+(i%2?8:0), y+i/2, color);
                        }
                    }
                }
                break;
        }
    }

    return width;
}

size_t BabelTypesetter::writeCodepoint(BABEL_CODEPOINT codepoint) {
    // TODO: RTL handling, word wrap, combining marks, etc.
    BabelGlyph glyph;
    if(codepoint == '\n') {
        this->cursor_x = 0; // (this->direction == 1) ? 0 : (this->_width - 8);
        this->cursor_y += 16;
    } else if(codepoint == '\r') {
        return 0;
    } else if (this->glyphStorage->fetch_glyph_data(codepoint, &glyph)) {
        int width = BABEL_INFO_GET_GLYPH_WIDTH(glyph.info);
        // word wrap should go here
        int xPos = (this->cursor_x + width * this->direction);
        int advance = drawGlyph(this->cursor_x, this->cursor_y, glyph, this->textColor);
        this->cursor_x += advance * this->direction;    // Advance x one char
        
        return 1;
    }

    return 0;
}
