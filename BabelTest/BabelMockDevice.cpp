//
//  BabelMockDevice.cpp
//  BabelTest
//
//  Created by Joey Castillo on 9/18/19.
//  Copyright © 2019 Joey Castillo. All rights reserved.
//

#include "BabelMockDevice.h"

BabelMockDevice::BabelMockDevice(const char *filename) {
    this->filename = filename;
}

BabelMockDevice::~BabelMockDevice() {
    fclose(this->file);
}

void BabelMockDevice::begin() {
    this->file = fopen(this->filename, "r");
    BabelDevice::begin();
}

void BabelMockDevice::read(uint32_t addr, void *data, uint32_t len) {
    fseek(this->file, addr, SEEK_SET);
    fread(data, sizeof(uint8_t), len, this->file);
}
