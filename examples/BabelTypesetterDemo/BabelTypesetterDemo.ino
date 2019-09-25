#define ENABLE_GxEPD2_GFX 0

#include <GxEPD2_BW.h>
#include <GxEPD2_3C.h>
#include <Fonts/FreeMonoBold9pt7b.h>

#include "BabelSPIFlash.h"
#include "BabelTypesetterGFX.h"

#define MAX_DISPAY_BUFFER_SIZE 15000ul // ~15k is a good compromise
#define MAX_HEIGHT(EPD) (EPD::HEIGHT <= MAX_DISPAY_BUFFER_SIZE / (EPD::WIDTH / 8) ? EPD::HEIGHT : MAX_DISPAY_BUFFER_SIZE / (EPD::WIDTH / 8))
GxEPD2_BW<GxEPD2_420, MAX_HEIGHT(GxEPD2_420)> display(GxEPD2_420(/*CS=77*/ 9, /*DC=*/ 10, /*RST=*/ A4, /*BUSY=*/ A3));

BabelTypesetterGFX typesetter(&display, 4, &SPI);

void setup(void) {
  Serial.begin(9600);
  Serial.print("Babel codepoint test!");
  display.init(115200);
  display.setRotation(3);
  typesetter.begin();
  typesetter.textColor = GxEPD_BLACK;
//  while(!Serial);
}

void loop() {
  Serial.println("clearing");
  display.fillScreen(GxEPD_WHITE);
  for (int block = 0; block <= 0xFF00; block += 0x100) {
    Serial.print("dumping block ");
    Serial.println(block >> 8);
    for (int i = 0; i <= 0xFF; i++) {
      if ((i % 16 == 0) && i > 0) {
        typesetter.writeCodepoint('\n');
//        typesetter.textSize = ((i / 16) % 5) + 1;
      }
      typesetter.writeCodepoint(block | i);
    }
    while (display.nextPage());
    Serial.println("drawn, wait");
    delay(1000);
    typesetter.setCursor(0, 0);
    display.fillScreen(GxEPD_WHITE);
  }
  Serial.println("moveon");
  delay(2000);
}
