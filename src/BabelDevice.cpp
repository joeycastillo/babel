//
//  BabelDevice.cpp
//  BabelTest
//
//  Created by Joey Castillo on 9/18/19.
//  Copyright © 2019 Joey Castillo. All rights reserved.
//

#include <string.h>
#include "BabelDevice.h"

void BabelDevice::begin() {
    this->read(BABEL_HEADER_LOC_WIDTH, &this->width, sizeof(this->width));
    this->read(BABEL_HEADER_LOC_HEIGHT, &this->height, sizeof(this->height));
    this->read(BABEL_HEADER_LOC_MAXGLYPH, &this->last_codepoint, sizeof(this->last_codepoint));
    this->read(BABEL_HEADER_LOC_START_OF_LUT, &this->location_of_lut, sizeof(this->location_of_lut));
    this->read(BABEL_HEADER_LOC_START_OF_META, &this->location_of_meta, sizeof(this->location_of_meta));
    this->read(BABEL_HEADER_LOC_START_OF_GLYPHS, &this->location_of_glyphs, sizeof(this->location_of_glyphs));
    uint32_t extra_loc = 0;
    uint32_t extra_len = 0;
    uint32_t currentPos = BABEL_HEADER_LOC_START_OF_EXTRAS;
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
}

uint32_t BabelDevice::get_last_available_codepoint() {
    return this->last_codepoint;
}

uint32_t BabelDevice::fetch_glyph_basic_info(uint32_t codepoint) {
    uint32_t loc = this->location_of_lut + codepoint * 4;
    uint32_t retVal;

    if (loc == 0) return false;
    this->read(loc, &retVal, 4);

    return retVal;
}

uint16_t BabelDevice::fetch_glyph_extended_info(uint32_t codepoint) {
    uint32_t loc = this->location_of_meta + codepoint * 2;
    uint16_t retVal;

    if (loc == 0) return false;
    this->read(loc, &retVal, 2);

    return retVal;
}

bool BabelDevice::fetch_glyph_data(uint32_t codepoint, BabelGlyph *glyph) {
    bool retVal = true;

    glyph->info = this->fetch_glyph_basic_info(codepoint);
    if (!glyph->info) {
        glyph->info = this->info_for_replacement_character;
        retVal = false;
    }
    
    uint32_t loc = BABEL_LUT_GET_GLYPH_LOCATION(glyph->info);

    if (BABEL_LUT_GET_GLYPH_WIDTH(glyph->info) == 16) {
        this->read(loc, &glyph->glyphData, 32);
        return retVal;
    } else {
        this->read(loc, &glyph->glyphData, 16);
        return retVal;
    }
}
