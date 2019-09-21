/*
 * The MIT License (MIT)
 *
 * Copyright © 2019 Joey Castillo. All rights reserved.
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
#include "BabelDevice.h"

#define BABEL_HEADER_LOC_RESERVED 0
#define BABEL_HEADER_LOC_VERSION 2
#define BABEL_HEADER_LOC_WIDTH 4
#define BABEL_HEADER_LOC_HEIGHT 5
#define BABEL_HEADER_LOC_FLAGS 6
#define BABEL_HEADER_LOC_MAXGLYPH 8
#define BABEL_HEADER_LOC_START_OF_LUT 12
#define BABEL_HEADER_LOC_START_OF_GLYPHS 16
#define BABEL_HEADER_LOC_START_OF_EXTRAS 20

#define BABEL_HEADER_EXTRA_TYPE_UPPERCASE_MAPPINGS 1
#define BABEL_HEADER_EXTRA_TYPE_LOWERCASE_MAPPINGS 2
#define BABEL_HEADER_EXTRA_TYPE_TITLECASE_MAPPINGS 3
#define BABEL_HEADER_EXTRA_TYPE_MIRRORING_MAPPINGS 4


void BabelDevice::begin() {
    this->read(BABEL_HEADER_LOC_WIDTH, &this->width, sizeof(this->width));
    this->read(BABEL_HEADER_LOC_HEIGHT, &this->height, sizeof(this->height));
    this->read(BABEL_HEADER_LOC_MAXGLYPH, &this->last_codepoint, sizeof(this->last_codepoint));
    this->read(BABEL_HEADER_LOC_START_OF_LUT, &this->location_of_lut, sizeof(this->location_of_lut));
    this->read(BABEL_HEADER_LOC_START_OF_GLYPHS, &this->location_of_glyphs, sizeof(this->location_of_glyphs));
    this->read(BABEL_HEADER_LOC_START_OF_EXTRAS, &this->location_of_extras, sizeof(this->location_of_extras));
    uint32_t extra_loc = 0;
    uint32_t extra_len = 0;
    uint32_t currentPos = this->location_of_extras;
    do {
        this->read(currentPos, &extra_loc, sizeof(extra_loc));
        currentPos += sizeof(extra_loc);
        this->read(currentPos, &extra_len, sizeof(extra_loc));
        currentPos += sizeof(extra_len);
        switch (extra_loc & 0xFF) {
        case BABEL_HEADER_EXTRA_TYPE_UPPERCASE_MAPPINGS:
            this->start_of_uppercase_mapping = extra_loc >> 8;
            this->end_of_uppercase_mapping = (extra_loc >> 8) + (extra_len >> 8);
            break;
        case BABEL_HEADER_EXTRA_TYPE_LOWERCASE_MAPPINGS:
            this->start_of_lowercase_mapping = extra_loc >> 8;
            this->end_of_lowercase_mapping = (extra_loc >> 8) + (extra_len >> 8);
            break;
        case BABEL_HEADER_EXTRA_TYPE_TITLECASE_MAPPINGS:
            this->start_of_titlecase_mapping = extra_loc >> 8;
            this->end_of_titlecase_mapping = (extra_loc >> 8) + (extra_len >> 8);
            break;
        case BABEL_HEADER_EXTRA_TYPE_MIRRORING_MAPPINGS:
            this->start_of_mirrored_mapping = extra_loc >> 8;
            this->end_of_mirrored_mapping = (extra_loc >> 8) + (extra_len >> 8);
            break;
        }
    } while(extra_loc && (currentPos < 256));
    
    this->info_for_replacement_character = this->fetch_glyph_basic_info(0xFFFD);
    this->extended_info_for_replacement_character = this->fetch_glyph_extended_info(0xFFFD);
}

BABEL_CODEPOINT BabelDevice::get_last_available_codepoint() {
    return this->last_codepoint;
}

uint32_t BabelDevice::fetch_glyph_basic_info(BABEL_CODEPOINT codepoint) {
    uint32_t retVal;
    uint32_t loc = this->location_of_lut + codepoint * 6;

    this->read(loc, &retVal, 4);

    return retVal;
}

uint16_t BabelDevice::fetch_glyph_extended_info(BABEL_CODEPOINT codepoint) {
    uint16_t retVal;
    uint32_t loc = 4 + this->location_of_lut + codepoint * 6;

    this->read(loc, &retVal, 2);

    return retVal;
}

bool BabelDevice::fetch_glyph_data(BABEL_CODEPOINT codepoint, BabelGlyph *glyph) {
    bool retVal = true;
    uint32_t loc = this->location_of_lut + codepoint * 6;

    // don't bother looking up out-of-range codepoints
    if (codepoint > this->last_codepoint) glyph->info = 0;
    else this->read(loc, glyph, 6);

    if (!glyph->info) {
        glyph->info = this->info_for_replacement_character;
        glyph->extendedInfo = this->extended_info_for_replacement_character;
        retVal = false;
    }
    
    loc = BABEL_INFO_GET_GLYPH_LOCATION(glyph->info);

    if (BABEL_INFO_GET_GLYPH_WIDTH(glyph->info) == 16) {
        this->read(loc, &glyph->glyphData, 32);
        return retVal;
    } else {
        this->read(loc, &glyph->glyphData, 16);
        return retVal;
    }
}
