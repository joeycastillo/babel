//
//  BabelSPIFlash.cpp
//  BabelTest
//
//  Created by Joey Castillo on 9/18/19.
//  Copyright © 2019 Joey Castillo. All rights reserved.
//

#include "BabelSPIFlash.h"

BabelSPIFlash::BabelSPIFlash(uint8_t cs, SPIClass *spi) {
    this->cs = cs;
    this->spi = spi;
}

BabelSPIFlash::~BabelSPIFlash() {
}

void BabelSPIFlash::begin() {
    Adafruit_FlashTransport_SPI flashTransport(this->cs, this->spi);
    Adafruit_SPIFlash flash(&flashTransport);
    this->flash = &flash;
    this->flash->begin();
    BabelDevice::begin();
}


void BabelSPIFlash::read(uint32_t addr, void *data, uint32_t len) {
    this->flash->readBuffer(addr, (uint8_t*)data, len);
}
