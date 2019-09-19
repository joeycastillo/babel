#include "BabelSPIFlash.h"

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  while(!Serial);
  digitalWrite(LED_BUILTIN, LOW);
  // eBook wing stuff, suppress SD card and eInk screen
  pinMode(5, OUTPUT);
  digitalWrite(5, HIGH);
  pinMode(9, OUTPUT);
  digitalWrite(9, HIGH);

  Serial.println("Babel example");
  Adafruit_FlashTransport_SPI flashTransport(4, &SPI);
  Adafruit_SPIFlash flash(&flashTransport);
  flash.begin();
  Serial.print("JEDEC ID: "); Serial.println(flash.getJEDECID(), HEX);
  Serial.print("Flash size: "); Serial.println(flash.size());
  BabelSPIFlash babel(&flash);
  BabelGlyph glyph;
  babel.begin();
  int last = babel.get_last_available_codepoint();
  for (int codepoint = 0; codepoint <= last; codepoint++) {
    if (babel.fetch_glyph_data(codepoint, &glyph)) {
      uint16_t extended = babel.fetch_glyph_extended_info(codepoint);
      uint32_t width = BABEL_LUT_GET_GLYPH_WIDTH(glyph.info);
//      drawGlyph(glyph);
      Serial.print("codepoint ");
      Serial.print(codepoint, HEX);
      Serial.print(" has width ");
      Serial.println(width);
      Serial.print("basic info ");
      Serial.println(glyph.info, HEX);
      if (BABEL_LUT_GET_CONTROL_CHARACTER(glyph.info)) Serial.println("It is a control character.");
      if (BABEL_LUT_GET_MARK_IS_COMBINING(glyph.info)) Serial.println("It is a combining or enclosing mark.");
      if (BABEL_LUT_GET_LINEBREAK_OPPORTUNITY(glyph.info)) Serial.println("You can break after this character.");
      if (BABEL_LUT_GET_STRONG_LTR(glyph.info)) Serial.println("It has a strong LTR affinity.");
      else if (BABEL_LUT_GET_STRONG_RTL(glyph.info)) Serial.println("It has a strong LTR affinity.");
      else Serial.println("It has no directional affinity.");
      Serial.print("extended info ");
      Serial.println(extended, HEX);
      if (BABEL_LUT_GET_MIRRORED_IN_RTL(glyph.info))
      {
        Serial.println("It is mirrored in RTL mode.");
        if BABEL_META_GET_HAS_BIDI_MIRRORING_MAPPING(extended) {
          Serial.println("And it has a mirrored glyph available.");
        } else {
          Serial.println("But it has no mirrored glyph! We'll have to improvise.");
        }
      }
      if BABEL_META_GET_HAS_LOWERCASE_MAPPING(extended) Serial.println("It has mapping to lowercase.");
      if BABEL_META_GET_HAS_UPPERCASE_MAPPING(extended) Serial.println("It has mapping to UPPERCASE.");
      if BABEL_META_GET_HAS_TITLECASE_MAPPING(extended) Serial.println("It has mapping to Titlecase.");
      if BABEL_META_GET_IS_WHITESPACE(extended) Serial.println("It is a whitespace character.");
      Serial.println("Its category is: ");
      switch (BABEL_META_GET_CHAR_CATEGORY(extended)) {
        case BABEL_CHAR_CATEGORY_LETTER_UPPERCASE:
        Serial.println("CHAR_CATEGORY_LETTER_UPPERCASE");
        break;
        case BABEL_CHAR_CATEGORY_LETTER_LOWERCASE:
        Serial.println("CHAR_CATEGORY_LETTER_LOWERCASE");
        break;
        case BABEL_CHAR_CATEGORY_LETTER_TITLECASE:
        Serial.println("CHAR_CATEGORY_LETTER_TITLECASE");
        break;
        case BABEL_CHAR_CATEGORY_LETTER_MODIFIER:
        Serial.println("CHAR_CATEGORY_LETTER_MODIFIER");
        break;
        case BABEL_CHAR_CATEGORY_LETTER_OTHER:
        Serial.println("CHAR_CATEGORY_LETTER_OTHER");
        break;
        case BABEL_CHAR_CATEGORY_MARK_NONSPACING:
        Serial.println("CHAR_CATEGORY_MARK_NONSPACING");
        break;
        case BABEL_CHAR_CATEGORY_MARK_SPACING_COMBINING:
        Serial.println("CHAR_CATEGORY_MARK_SPACING_COMBINING");
        break;
        case BABEL_CHAR_CATEGORY_MARK_ENCLOSING:
        Serial.println("CHAR_CATEGORY_MARK_ENCLOSING");
        break;
        case BABEL_CHAR_CATEGORY_NUMBER_DECIMAL_DIGIT:
        Serial.println("CHAR_CATEGORY_NUMBER_DECIMAL_DIGIT");
        break;
        case BABEL_CHAR_CATEGORY_NUMBER_LETTER:
        Serial.println("CHAR_CATEGORY_NUMBER_LETTER");
        break;
        case BABEL_CHAR_CATEGORY_NUMBER_OTHER:
        Serial.println("CHAR_CATEGORY_NUMBER_OTHER");
        break;
        case BABEL_CHAR_CATEGORY_PUNCTUATION_CONNECTOR:
        Serial.println("CHAR_CATEGORY_PUNCTUATION_CONNECTOR");
        break;
        case BABEL_CHAR_CATEGORY_PUNCTUATION_DASH:
        Serial.println("CHAR_CATEGORY_PUNCTUATION_DASH");
        break;
        case BABEL_CHAR_CATEGORY_PUNCTUATION_OPEN:
        Serial.println("CHAR_CATEGORY_PUNCTUATION_OPEN");
        break;
        case BABEL_CHAR_CATEGORY_PUNCTUATION_CLOSE:
        Serial.println("CHAR_CATEGORY_PUNCTUATION_CLOSE");
        break;
        case BABEL_CHAR_CATEGORY_PUNCTUATION_INITIAL_QUOTE:
        Serial.println("CHAR_CATEGORY_PUNCTUATION_INITIAL_QUOTE");
        break;
        case BABEL_CHAR_CATEGORY_PUNCTUATION_FINAL_QUOTE:
        Serial.println("CHAR_CATEGORY_PUNCTUATION_FINAL_QUOTE");
        break;
        case BABEL_CHAR_CATEGORY_PUNCTUATION_OTHER:
        Serial.println("CHAR_CATEGORY_PUNCTUATION_OTHER");
        break;
        case BABEL_CHAR_CATEGORY_SYMBOL_MATH:
        Serial.println("CHAR_CATEGORY_SYMBOL_MATH");
        break;
        case BABEL_CHAR_CATEGORY_SYMBOL_CURRENCY:
        Serial.println("CHAR_CATEGORY_SYMBOL_CURRENCY");
        break;
        case BABEL_CHAR_CATEGORY_SYMBOL_MODIFIER:
        Serial.println("CHAR_CATEGORY_SYMBOL_MODIFIER");
        break;
        case BABEL_CHAR_CATEGORY_SYMBOL_OTHER:
        Serial.println("CHAR_CATEGORY_SYMBOL_OTHER");
        break;
        case BABEL_CHAR_CATEGORY_SEPARATOR_SPACE:
        Serial.println("CHAR_CATEGORY_SEPARATOR_SPACE");
        break;
        case BABEL_CHAR_CATEGORY_SEPARATOR_LINE:
        Serial.println("CHAR_CATEGORY_SEPARATOR_LINE");
        break;
        case BABEL_CHAR_CATEGORY_SEPARATOR_PARAGRAPH:
        Serial.println("CHAR_CATEGORY_SEPARATOR_PARAGRAPH");
        break;
        case BABEL_CHAR_CATEGORY_OTHER_CONTROL:
        Serial.println("CHAR_CATEGORY_OTHER_CONTROL");
        break;
        case BABEL_CHAR_CATEGORY_OTHER_FORMAT:
        Serial.println("CHAR_CATEGORY_OTHER_FORMAT");
        break;
        case BABEL_CHAR_CATEGORY_OTHER_SURROGATE:
        Serial.println("CHAR_CATEGORY_OTHER_SURROGATE");
        break;
        case BABEL_CHAR_CATEGORY_OTHER_PRIVATE_USE:
        Serial.println("CHAR_CATEGORY_OTHER_PRIVATE_USE");
        break;
        case BABEL_CHAR_CATEGORY_OTHER_NOT_ASSIGNED:
        Serial.println("CHAR_CATEGORY_OTHER_NOT_ASSIGNED");
        break;
        default:
        Serial.println("UNKNOWN?!");
      }
      Serial.println();
      Serial.println("Its bidi class is: ");
      switch (BABEL_META_GET_BIDI_CLASS(extended)) {
        case BABEL_BIDI_CLASS_LEFT_TO_RIGHT:
        Serial.println("BIDI_CLASS_LEFT_TO_RIGHT");
        break;
        case BABEL_BIDI_CLASS_RIGHT_TO_LEFT:
        Serial.println("BIDI_CLASS_RIGHT_TO_LEFT");
        break;
        case BABEL_BIDI_CLASS_ARABIC_LETTER:
        Serial.println("BIDI_CLASS_ARABIC_LETTER");
        break;
        case BABEL_BIDI_CLASS_EUROPEAN_NUMBER:
        Serial.println("BIDI_CLASS_EUROPEAN_NUMBER");
        break;
        case BABEL_BIDI_CLASS_EUROPEAN_SEPARATOR:
        Serial.println("BIDI_CLASS_EUROPEAN_SEPARATOR");
        break;
        case BABEL_BIDI_CLASS_EUROPEAN_NUMBER_TERMINATOR:
        Serial.println("BIDI_CLASS_EUROPEAN_NUMBER_TERMINATOR");
        break;
        case BABEL_BIDI_CLASS_ARABIC_NUMBER:
        Serial.println("BIDI_CLASS_ARABIC_NUMBER");
        break;
        case BABEL_BIDI_CLASS_COMMON_NUMBER_SEPARATOR:
        Serial.println("BIDI_CLASS_COMMON_NUMBER_SEPARATOR");
        break;
        case BABEL_BIDI_CLASS_NONSPACING_MARK:
        Serial.println("BIDI_CLASS_NONSPACING_MARK");
        break;
        case BABEL_BIDI_CLASS_BOUNDARY_NEUTRAL:
        Serial.println("BIDI_CLASS_BOUNDARY_NEUTRAL");
        break;
        case BABEL_BIDI_CLASS_PARAGRAPH_SEPARATOR:
        Serial.println("BIDI_CLASS_PARAGRAPH_SEPARATOR");
        break;
        case BABEL_BIDI_CLASS_SEGMENT_SEPARATOR:
        Serial.println("BIDI_CLASS_SEGMENT_SEPARATOR");
        break;
        case BABEL_BIDI_CLASS_WHITESPACE:
        Serial.println("BIDI_CLASS_WHITESPACE");
        break;
        case BABEL_BIDI_CLASS_OTHER_NEUTRALS:
        Serial.println("BIDI_CLASS_OTHER_NEUTRALS");
        break;
        case BABEL_BIDI_CLASS_DIRECTIONAL_CONTROL_CHARACTER:
        Serial.println("BIDI_CLASS_DIRECTIONAL_CONTROL_CHARACTER");
        break;
        default:
        Serial.println("UNKNOWN?!?!");
      }
      Serial.println();
    } else {
      Serial.print("codepoint ");
      Serial.print(codepoint);
      Serial.println(" is not a valid Unicode character.");
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
