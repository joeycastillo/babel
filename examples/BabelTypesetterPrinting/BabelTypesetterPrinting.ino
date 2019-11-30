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

//BABEL_CODEPOINT string[] =  {0x0048, 0x0065, 0x006C, 0x006C, 0x006F, 0x0020, 0x0057, 0x006F, 0x0072, 0x006C, 0x0064, 0x0021, 0x000A, 0x05E9, 0x05DC, 0x05D5, 0x05DD, 0x0020, 0x05E2, 0x05D5, 0x05DC, 0x05DD, 0x000A, 0x041F, 0x0440, 0x0438, 0x0432, 0x0435, 0x0442, 0x002C, 0x0020, 0x043C, 0x0438, 0x0440, 0x0021, 0x000A, 0xFEE3, 0xFEAE, 0xFEA3, 0xFE92, 0xFE8E, 0x0020, 0xFE91, 0xFE8E, 0xFEDF, 0xFECC, 0xFE8E, 0xFEDF, 0xFEE2, 0x000A, 0x0020, 0x0048, 0x006F, 0x006C, 0x0061, 0x0020, 0x004D, 0x0075, 0x006E, 0x0064, 0x006F, 0x0021, 0x000A};

void loop() {
  Serial.println("clearing");
  display.fillScreen(GxEPD_WHITE);
  typesetter.setCursor(16, 16);
  typesetter.print("Voici mon secret. Il est très \nsimple: on ne voit bien qu'avec \nle cœur. L'essentiel est \ninvisible pour les yeux.");
  while (display.nextPage());
  Serial.println("drawn, wait");
  delay(1000);
  display.fillScreen(GxEPD_WHITE);
  Serial.println("moveon");
  delay(2000);
}
