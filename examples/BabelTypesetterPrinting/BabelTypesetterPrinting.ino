// For use with the eBook Wing. Assumes Babel chip select is on D4.
// For demo using the Open Book, check its repository: 
// https://github.com/joeycastillo/The-Open-Book

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
  typesetter.setTextColor(GxEPD_BLACK);
  typesetter.setLayoutArea(16, 16, 264, 368);
//  while(!Serial);
}

void loop() {
  Serial.println("clearing");
  display.fillScreen(GxEPD_WHITE);
  typesetter.resetCursor();
  typesetter.print("Voici mon secret. Il est très \nsimple: on ne voit bien qu'avec \nle cœur. L'essentiel est \ninvisible pour les yeux.");
  while (display.nextPage());
  Serial.println("drawn, wait");
  delay(3000);
}
