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

#ifndef BabelMacros_h
#define BabelMacros_h

#define BABEL_LUT_GET_GLYPH_LOCATION(x) (x & 0x3FFFFF)
#define BABEL_LUT_GET_GLYPH_WIDTH(x) ((x >> 22) & 0x1F)
#define BABEL_LUT_GET_MARK_IS_COMBINING(x) (x & 0x8000000)
#define BABEL_LUT_GET_MIRRORED_IN_RTL(x) (__builtin_popcount(x & 0x30000000) == 2)
#define BABEL_LUT_GET_STRONG_RTL(x) ((x & 0x10000000) && (__builtin_popcount(x & 0x30000000) == 1))
#define BABEL_LUT_GET_STRONG_LTR(x) ((x & 0x20000000) && (__builtin_popcount(x & 0x30000000) == 1))
#define BABEL_LUT_GET_CONTROL_CHARACTER(x) (x & 0x40000000)
#define BABEL_LUT_GET_LINEBREAK_OPPORTUNITY(x) (x & 0x80000000)

#define BABEL_META_GET_CHAR_CATEGORY(x) (x & 0x1F)
#define BABEL_META_GET_HAS_UPPERCASE_MAPPING(x) (x & 0x20)
#define BABEL_META_GET_HAS_LOWERCASE_MAPPING(x) (x & 0x40)
#define BABEL_META_GET_HAS_TITLECASE_MAPPING(x) (x & 0x80)
#define BABEL_META_GET_BIDI_CLASS(x) ((x >> 8) & 0xF)
#define BABEL_META_GET_HAS_BIDI_MIRRORING_MAPPING(x) (x & 0x1000)
#define BABEL_META_GET_IS_WHITESPACE(x) (x & 0x2000)

#define BABEL_CHAR_CATEGORY_LETTER_UPPERCASE 1
#define BABEL_CHAR_CATEGORY_LETTER_LOWERCASE 2
#define BABEL_CHAR_CATEGORY_LETTER_TITLECASE 3
#define BABEL_CHAR_CATEGORY_LETTER_MODIFIER 4
#define BABEL_CHAR_CATEGORY_LETTER_OTHER 5
#define BABEL_CHAR_CATEGORY_MARK_NONSPACING 6
#define BABEL_CHAR_CATEGORY_MARK_SPACING_COMBINING 7
#define BABEL_CHAR_CATEGORY_MARK_ENCLOSING 8
#define BABEL_CHAR_CATEGORY_NUMBER_DECIMAL_DIGIT 9
#define BABEL_CHAR_CATEGORY_NUMBER_LETTER 10
#define BABEL_CHAR_CATEGORY_NUMBER_OTHER 11
#define BABEL_CHAR_CATEGORY_PUNCTUATION_CONNECTOR 12
#define BABEL_CHAR_CATEGORY_PUNCTUATION_DASH 13
#define BABEL_CHAR_CATEGORY_PUNCTUATION_OPEN 14
#define BABEL_CHAR_CATEGORY_PUNCTUATION_CLOSE 15
#define BABEL_CHAR_CATEGORY_PUNCTUATION_INITIAL_QUOTE 16
#define BABEL_CHAR_CATEGORY_PUNCTUATION_FINAL_QUOTE 17
#define BABEL_CHAR_CATEGORY_PUNCTUATION_OTHER 18
#define BABEL_CHAR_CATEGORY_SYMBOL_MATH 19
#define BABEL_CHAR_CATEGORY_SYMBOL_CURRENCY 20
#define BABEL_CHAR_CATEGORY_SYMBOL_MODIFIER 21
#define BABEL_CHAR_CATEGORY_SYMBOL_OTHER 22
#define BABEL_CHAR_CATEGORY_SEPARATOR_SPACE 23
#define BABEL_CHAR_CATEGORY_SEPARATOR_LINE 24
#define BABEL_CHAR_CATEGORY_SEPARATOR_PARAGRAPH 25
#define BABEL_CHAR_CATEGORY_OTHER_CONTROL 26
#define BABEL_CHAR_CATEGORY_OTHER_FORMAT 27
#define BABEL_CHAR_CATEGORY_OTHER_SURROGATE 28
#define BABEL_CHAR_CATEGORY_OTHER_PRIVATE_USE 29
#define BABEL_CHAR_CATEGORY_OTHER_NOT_ASSIGNED 30

#define BABEL_BIDI_CLASS_LEFT_TO_RIGHT 1
#define BABEL_BIDI_CLASS_RIGHT_TO_LEFT 2
#define BABEL_BIDI_CLASS_ARABIC_LETTER 3
#define BABEL_BIDI_CLASS_EUROPEAN_NUMBER 4
#define BABEL_BIDI_CLASS_EUROPEAN_SEPARATOR 5
#define BABEL_BIDI_CLASS_EUROPEAN_NUMBER_TERMINATOR 6
#define BABEL_BIDI_CLASS_ARABIC_NUMBER 7
#define BABEL_BIDI_CLASS_COMMON_NUMBER_SEPARATOR 8
#define BABEL_BIDI_CLASS_NONSPACING_MARK 9
#define BABEL_BIDI_CLASS_BOUNDARY_NEUTRAL 10
#define BABEL_BIDI_CLASS_PARAGRAPH_SEPARATOR 11
#define BABEL_BIDI_CLASS_SEGMENT_SEPARATOR 12
#define BABEL_BIDI_CLASS_WHITESPACE 13
#define BABEL_BIDI_CLASS_OTHER_NEUTRALS 14
#define BABEL_BIDI_CLASS_DIRECTIONAL_CONTROL_CHARACTER 15
#endif /* BabelMacros_h */
