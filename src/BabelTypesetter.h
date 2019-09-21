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

#ifndef BabelTypesetter_h
#define BabelTypesetter_h

#include <stdio.h>
#include <stdint.h>
#include "BabelDevice.h"

class BabelTypesetter {
public:
    BabelTypesetter();
    virtual void begin();
    /**
     @brief Pure virtual method for drawing a pixel. All glyph drawing methods call this to push pixels.
     @param x pixel's X coordinate
     @param y pixel's Y coordinate
     @param color 16-bit pixel color
    */
    virtual void drawPixel(int16_t x, int16_t y, uint16_t color) = 0;    ///< Virtual drawPixel() function to draw to the screen/framebuffer/etc, must be overridden in subclass. 

    /**
     @brief Virtual method for drawing a rect. You may override this if you have a more efficient implementation.
     @param x origin X coordinate
     @param y origin Y coordinate
     @param w rect width
     @param h rect height
     @param color 16-bit pixel color
    */
    virtual void drawFillRect(int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color);

    /**
    /*!
     @brief sets cursor position
     @param x x coordinate
     @param y y coordinate
    */
    /**************************************************************************/
    void setCursor(int16_t x, int16_t y);
    /**
     @brief Draws a glyph at the given coordinates.
     @param x X coordinate of the glyph.
     @param y Y coordinate of the glyph.
     @param glyph The glyph you wish to draw.
     @param color 16-bit pixel color
     @returns the width of the glyph that was drawn. Can be zero.
     @note This method simply draws the glyph; it does not touch layout direction or cursor position.
    */
    int drawGlyph(int16_t x, int16_t y, BabelGlyph glyph, uint16_t color);
    /**
     @brief Writes a glyph at the current cursor position
     @param codepoint The codepoint you wish to draw. Not UTF-8. Not UTF-16. The codepoint itself.
     @returns the number 1 if a codepoint was written, 0 if one was not.
     @note This method handles newlines and direction changes, and updates the current cursor position. It might move 8 or 16 pixels to the right, OR it might move to the left side of the next line if the text wrapped. But it could also move to the right side of the next line if the layout direction changed to RTL mode.
    */
    size_t writeCodepoint(uint32_t codepoint);

    BabelDevice *glyphStorage = NULL;
    uint16_t textColor = 0;      ///< 16-bit background color for print()
protected:
    int16_t cursor_x = 0;       ///< x location to start print()ing text
    int16_t cursor_y = 0;       ///< y location to start print()ing text
private:
    int8_t  direction = 1; ///< 1 for LTR, -1 for RTL.
};

#endif /* BabelTypesetter_h */
