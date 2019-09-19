//
//  BabelDevice.h
//  BabelTest
//
//  Created by Joey Castillo on 9/18/19.
//  Copyright © 2019 Joey Castillo. All rights reserved.
//

#ifndef BabelDevice_h
#define BabelDevice_h

#include <stdio.h>
#include <stdint.h>
#include "BabelMacros.h"

struct BabelGlyph {
    uint32_t info;
    uint8_t glyphData[32];
};

class BabelDevice {
public:
    void begin();
    /**
     @brief Returns the last codepoint that is available on the device. Implementations should not request codepoints higher than this.
    */
    uint32_t get_last_available_codepoint();
    
    /**
     @brief This method seeks into a lookup table for basic data about the glyph. O(1) access time.
     @returns A uint32_t that contains the glyph's location on the device in the lower 22 bits, and some basic metadata in the higher 10 bits.
     @param codepoint The codepoint whose basic data you want to fetch.
     @note The macros in BabelMacros.h help to get the desired data out of this value.
     @see BABEL_LUT_GET_GLYPH_LOCATION
     @see BABEL_LUT_GET_GLYPH_WIDTH
     @see BABEL_LUT_GET_MARK_IS_COMBINING
     @see BABEL_LUT_GET_MIRRORED_IN_RTL
     @see BABEL_LUT_GET_STRONG_RTL
     @see BABEL_LUT_GET_STRONG_LTR
     @see BABEL_LUT_GET_CONTROL_CHARACTER
     @see BABEL_LUT_GET_LINEBREAK_OPPORTUNITY
    */
    uint32_t fetch_glyph_basic_info(uint32_t codepoint);
    
    /**
     @brief This method seeks into a secondary lookup table for more detailed data about the glyph. O(1) access time.
     @returns A uint16_t that contains a 5-bit value for the character's general category, a 4-bit value for the character's bidirectional class, and several flags that indicate the presence of mappings.
     @param codepoint The codepoint whose extended data you want to fetch.
     @note The macros in BabelMacros.h help to get the desired data out of this value.
     @see BABEL_META_GET_CHAR_CATEGORY
     @see BABEL_META_GET_BIDI_CLASS
     @see BABEL_META_GET_HAS_UPPERCASE_MAPPING
     @see BABEL_META_GET_HAS_LOWERCASE_MAPPING
     @see BABEL_META_GET_HAS_TITLECASE_MAPPING
     @see BABEL_META_GET_HAS_BIDI_MIRRORING_MAPPING
     @see BABEL_META_GET_IS_WHITESPACE
    */
    uint16_t fetch_glyph_extended_info(uint32_t codepoint);
    
    /**
     @brief This method first calls fetch_glyph_basic_info to populate the struct's info field, which includes the glyph data's location. It then seeks to that location and populates the struct's glyphData field with the glyph bitmap.
     @returns true if the codepoint was valid; false if it was invalid. If false, the glyph struct will contain data and graphics for codepoint U+FFFD "REPLACEMENT CHARACTER"
     @param codepoint The codepoint whose data you want to fetch.
     @param glyph Output parameter, the struct you wish to populate with data.
     @note If the glyph is only 16 bytes, this method will populate the first 16 bytes of glyphData, and leave the rest alone. In this case, you can expect a width value in info that is <= 8.
    */
    bool fetch_glyph_data(uint32_t codepoint, BabelGlyph *glyph);
protected:
    virtual void read(uint32_t addr, void *data, uint32_t len) = 0;
private:
    uint8_t width = 0;
    uint8_t height = 0;
    uint32_t last_codepoint = 0;
    uint32_t location_of_lut = 0;
    uint32_t location_of_meta = 0;
    uint32_t location_of_glyphs = 0;
    uint32_t location_of_extras = 0;
    uint32_t start_of_uppercase_mapping = 0;
    uint32_t start_of_lowercase_mapping = 0;
    uint32_t start_of_titlecase_mapping = 0;
    uint32_t start_of_mirrored_mapping = 0;
    uint32_t end_of_uppercase_mapping = 0;
    uint32_t end_of_lowercase_mapping = 0;
    uint32_t end_of_titlecase_mapping = 0;
    uint32_t end_of_mirrored_mapping = 0;
    uint32_t info_for_replacement_character = 0;
};

#endif /* BabelDevice_h */
