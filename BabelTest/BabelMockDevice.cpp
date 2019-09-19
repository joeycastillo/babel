//
//  BabelMockDevice.cpp
//  BabelTest
//
//  Created by Joey Castillo on 9/18/19.
//  Copyright © 2019 Joey Castillo. All rights reserved.
//

#include "BabelMockDevice.h"
#include <iostream>

using namespace std;

BabelMockDevice::BabelMockDevice(const char *filename) {
    this->file = fopen(filename, "r");
}

BabelMockDevice::~BabelMockDevice() {
    fclose(this->file);
}

void BabelMockDevice::read(uint32_t addr, void *data, uint32_t len) {
    fseek(this->file, addr, SEEK_SET);
    fread(data, sizeof(uint8_t), len, this->file);
}
