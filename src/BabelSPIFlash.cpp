//
//  BabelSPIFlash.cpp
//  BabelTest
//
//  Created by Joey Castillo on 9/18/19.
//  Copyright © 2019 Joey Castillo. All rights reserved.
//

#include "BabelSPIFlash.h"

BabelSPIFlash::BabelSPIFlash(Adafruit_SPIFlash *flash) {
    this->flash = flash;
}

BabelSPIFlash::~BabelSPIFlash() {
}

void BabelSPIFlash::read(uint32_t addr, void *data, uint32_t len) {
    this->flash->readBuffer(addr, (uint8_t*)data, len);
}
