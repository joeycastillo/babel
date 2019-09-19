//
//  main.cpp
//  BabelTest
//
//  Created by Joey Castillo on 9/18/19.
//  Copyright © 2019 Joey Castillo. All rights reserved.
//

#include <iostream>
#include <bitset>
#include "BabelMockDevice.h"

using namespace std;

void drawGlyph(BabelGlyph glyph) {
    uint32_t width = BABEL_LUT_GET_GLYPH_WIDTH(glyph.info);
    if (width == 8) {
        for (int i = 0; i < 16; i++) {
            bitset<8> x(glyph.glyphData[i]);
            string s = x.to_string();
            size_t pos;
            while ((pos = s.find("0")) != std::string::npos) s.replace(pos, 1, " ");
            while ((pos = s.find("1")) != std::string::npos) s.replace(pos, 1, "#");
            cout << s << endl;
        }
    }
    if (width == 16) {
        for (int i = 0; i < 32; i += 2) {
            for (int j = 0; j < 2; j++) {
                bitset<8> x(glyph.glyphData[i + j]);
                string s = x.to_string();
                size_t pos;
                while ((pos = s.find("0")) != std::string::npos) s.replace(pos, 1, " ");
                while ((pos = s.find("1")) != std::string::npos) s.replace(pos, 1, "#");
                cout << s;
            }
            cout << endl;
        }
    }
}

int main(int argc, const char * argv[]) {
    if (argc != 2) {
        cout << "Usage: BabelTest /path/to/babel.bin" << endl;
        exit(1);
    }
    BabelMockDevice babel = BabelMockDevice(argv[1]);
    BabelGlyph glyph;
    babel.begin();
    uint32_t last_codepoint = babel.get_last_available_codepoint();
    for (uint32_t codepoint = 0x0000; codepoint <= last_codepoint; codepoint++) {
        if (babel.fetch_glyph_data(codepoint, &glyph))
        {
            uint16_t extended = babel.fetch_glyph_extended_info(codepoint);
            uint32_t width = BABEL_LUT_GET_GLYPH_WIDTH(glyph.info);
            drawGlyph(glyph);
            cout << "codepoint " << std::hex << codepoint << " has width " << std::dec << width << "." << endl;
            bitset<32> x(glyph.info);
            cout << "basic info " << hex << glyph.info << " - " << x << endl;
            if (BABEL_LUT_GET_CONTROL_CHARACTER(glyph.info)) cout << "It is a control character." << endl;
            if (BABEL_LUT_GET_MARK_IS_COMBINING(glyph.info)) cout << "It is a combining or enclosing mark." << endl;
            if (BABEL_LUT_GET_LINEBREAK_OPPORTUNITY(glyph.info)) cout << "You can break after this character." << endl;
            if (BABEL_LUT_GET_STRONG_LTR(glyph.info)) cout << "It has a strong LTR affinity." << endl;
            else if (BABEL_LUT_GET_STRONG_RTL(glyph.info)) cout << "It has a strong LTR affinity." << endl;
            else cout << "It has no directional affinity." << endl;
            bitset<16> y(extended);
            cout << "extended info " << hex << extended << " - " << y << endl;
            if (BABEL_LUT_GET_MIRRORED_IN_RTL(glyph.info))
            {
                cout << "It is mirrored in RTL mode." << endl;
                if BABEL_META_GET_HAS_BIDI_MIRRORING_MAPPING(extended) {
                    cout << "And it has a mirrored glyph available." << endl;
                } else {
                    cout << "But it has no mirrored glyph! We'll have to improvise." << endl;
                }
            }
            if BABEL_META_GET_HAS_LOWERCASE_MAPPING(extended) cout << "It has mapping to lowercase." << endl;
            if BABEL_META_GET_HAS_UPPERCASE_MAPPING(extended) cout << "It has mapping to UPPERCASE." << endl;
            if BABEL_META_GET_HAS_TITLECASE_MAPPING(extended) cout << "It has mapping to Titlecase." << endl;
            if BABEL_META_GET_IS_WHITESPACE(extended) cout << "It is a whitespace character." << endl;
            cout << "Its category is: ";
            switch (BABEL_META_GET_CHAR_CATEGORY(extended)) {
                case BABEL_CHAR_CATEGORY_LETTER_UPPERCASE:
                    cout << "CHAR_CATEGORY_LETTER_UPPERCASE";
                    break;
                case BABEL_CHAR_CATEGORY_LETTER_LOWERCASE:
                    cout << "CHAR_CATEGORY_LETTER_LOWERCASE";
                    break;
                case BABEL_CHAR_CATEGORY_LETTER_TITLECASE:
                    cout << "CHAR_CATEGORY_LETTER_TITLECASE";
                    break;
                case BABEL_CHAR_CATEGORY_LETTER_MODIFIER:
                    cout << "CHAR_CATEGORY_LETTER_MODIFIER";
                    break;
                case BABEL_CHAR_CATEGORY_LETTER_OTHER:
                    cout << "CHAR_CATEGORY_LETTER_OTHER";
                    break;
                case BABEL_CHAR_CATEGORY_MARK_NONSPACING:
                    cout << "CHAR_CATEGORY_MARK_NONSPACING";
                    break;
                case BABEL_CHAR_CATEGORY_MARK_SPACING_COMBINING:
                    cout << "CHAR_CATEGORY_MARK_SPACING_COMBINING";
                    break;
                case BABEL_CHAR_CATEGORY_MARK_ENCLOSING:
                    cout << "CHAR_CATEGORY_MARK_ENCLOSING";
                    break;
                case BABEL_CHAR_CATEGORY_NUMBER_DECIMAL_DIGIT:
                    cout << "CHAR_CATEGORY_NUMBER_DECIMAL_DIGIT";
                    break;
                case BABEL_CHAR_CATEGORY_NUMBER_LETTER:
                    cout << "CHAR_CATEGORY_NUMBER_LETTER";
                    break;
                case BABEL_CHAR_CATEGORY_NUMBER_OTHER:
                    cout << "CHAR_CATEGORY_NUMBER_OTHER";
                    break;
                case BABEL_CHAR_CATEGORY_PUNCTUATION_CONNECTOR:
                    cout << "CHAR_CATEGORY_PUNCTUATION_CONNECTOR";
                    break;
                case BABEL_CHAR_CATEGORY_PUNCTUATION_DASH:
                    cout << "CHAR_CATEGORY_PUNCTUATION_DASH";
                    break;
                case BABEL_CHAR_CATEGORY_PUNCTUATION_OPEN:
                    cout << "CHAR_CATEGORY_PUNCTUATION_OPEN";
                    break;
                case BABEL_CHAR_CATEGORY_PUNCTUATION_CLOSE:
                    cout << "CHAR_CATEGORY_PUNCTUATION_CLOSE";
                    break;
                case BABEL_CHAR_CATEGORY_PUNCTUATION_INITIAL_QUOTE:
                    cout << "CHAR_CATEGORY_PUNCTUATION_INITIAL_QUOTE";
                    break;
                case BABEL_CHAR_CATEGORY_PUNCTUATION_FINAL_QUOTE:
                    cout << "CHAR_CATEGORY_PUNCTUATION_FINAL_QUOTE";
                    break;
                case BABEL_CHAR_CATEGORY_PUNCTUATION_OTHER:
                    cout << "CHAR_CATEGORY_PUNCTUATION_OTHER";
                    break;
                case BABEL_CHAR_CATEGORY_SYMBOL_MATH:
                    cout << "CHAR_CATEGORY_SYMBOL_MATH";
                    break;
                case BABEL_CHAR_CATEGORY_SYMBOL_CURRENCY:
                    cout << "CHAR_CATEGORY_SYMBOL_CURRENCY";
                    break;
                case BABEL_CHAR_CATEGORY_SYMBOL_MODIFIER:
                    cout << "CHAR_CATEGORY_SYMBOL_MODIFIER";
                    break;
                case BABEL_CHAR_CATEGORY_SYMBOL_OTHER:
                    cout << "CHAR_CATEGORY_SYMBOL_OTHER";
                    break;
                case BABEL_CHAR_CATEGORY_SEPARATOR_SPACE:
                    cout << "CHAR_CATEGORY_SEPARATOR_SPACE";
                    break;
                case BABEL_CHAR_CATEGORY_SEPARATOR_LINE:
                    cout << "CHAR_CATEGORY_SEPARATOR_LINE";
                    break;
                case BABEL_CHAR_CATEGORY_SEPARATOR_PARAGRAPH:
                    cout << "CHAR_CATEGORY_SEPARATOR_PARAGRAPH";
                    break;
                case BABEL_CHAR_CATEGORY_OTHER_CONTROL:
                    cout << "CHAR_CATEGORY_OTHER_CONTROL";
                    break;
                case BABEL_CHAR_CATEGORY_OTHER_FORMAT:
                    cout << "CHAR_CATEGORY_OTHER_FORMAT";
                    break;
                case BABEL_CHAR_CATEGORY_OTHER_SURROGATE:
                    cout << "CHAR_CATEGORY_OTHER_SURROGATE";
                    break;
                case BABEL_CHAR_CATEGORY_OTHER_PRIVATE_USE:
                    cout << "CHAR_CATEGORY_OTHER_PRIVATE_USE";
                    break;
                case BABEL_CHAR_CATEGORY_OTHER_NOT_ASSIGNED:
                    cout << "CHAR_CATEGORY_OTHER_NOT_ASSIGNED";
                    break;
                default:
                    cout << "UNKNOWN?!";
                    abort();
            }
            cout << endl;
            cout << "Its bidi class is: ";
            switch (BABEL_META_GET_BIDI_CLASS(extended)) {
                case BABEL_BIDI_CLASS_LEFT_TO_RIGHT:
                    cout << "BIDI_CLASS_LEFT_TO_RIGHT";
                    break;
                case BABEL_BIDI_CLASS_RIGHT_TO_LEFT:
                    cout << "BIDI_CLASS_RIGHT_TO_LEFT";
                    break;
                case BABEL_BIDI_CLASS_ARABIC_LETTER:
                    cout << "BIDI_CLASS_ARABIC_LETTER";
                    break;
                case BABEL_BIDI_CLASS_EUROPEAN_NUMBER:
                    cout << "BIDI_CLASS_EUROPEAN_NUMBER";
                    break;
                case BABEL_BIDI_CLASS_EUROPEAN_SEPARATOR:
                    cout << "BIDI_CLASS_EUROPEAN_SEPARATOR";
                    break;
                case BABEL_BIDI_CLASS_EUROPEAN_NUMBER_TERMINATOR:
                    cout << "BIDI_CLASS_EUROPEAN_NUMBER_TERMINATOR";
                    break;
                case BABEL_BIDI_CLASS_ARABIC_NUMBER:
                    cout << "BIDI_CLASS_ARABIC_NUMBER";
                    break;
                case BABEL_BIDI_CLASS_COMMON_NUMBER_SEPARATOR:
                    cout << "BIDI_CLASS_COMMON_NUMBER_SEPARATOR";
                    break;
                case BABEL_BIDI_CLASS_NONSPACING_MARK:
                    cout << "BIDI_CLASS_NONSPACING_MARK";
                    break;
                case BABEL_BIDI_CLASS_BOUNDARY_NEUTRAL:
                    cout << "BIDI_CLASS_BOUNDARY_NEUTRAL";
                    break;
                case BABEL_BIDI_CLASS_PARAGRAPH_SEPARATOR:
                    cout << "BIDI_CLASS_PARAGRAPH_SEPARATOR";
                    break;
                case BABEL_BIDI_CLASS_SEGMENT_SEPARATOR:
                    cout << "BIDI_CLASS_SEGMENT_SEPARATOR";
                    break;
                case BABEL_BIDI_CLASS_WHITESPACE:
                    cout << "BIDI_CLASS_WHITESPACE";
                    break;
                case BABEL_BIDI_CLASS_OTHER_NEUTRALS:
                    cout << "BIDI_CLASS_OTHER_NEUTRALS";
                    break;
                case BABEL_BIDI_CLASS_DIRECTIONAL_CONTROL_CHARACTER:
                    cout << "BIDI_CLASS_DIRECTIONAL_CONTROL_CHARACTER";
                    break;
                default:
                    cout << "UNKNOWN?!?!";
                    abort();
            }
            cout << endl;
        } else {
            cout << "codepoint " << codepoint << " is not a valid Unicode character." << endl;
        }
        cout << endl << endl;
    }
    return 0;
}
