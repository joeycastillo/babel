//
//  BabelMockDevice.h
//  BabelTest
//
//  Created by Joey Castillo on 9/18/19.
//  Copyright © 2019 Joey Castillo. All rights reserved.
//

#ifndef BabelMockDevice_h
#define BabelMockDevice_h

#include <stdio.h>
#include "BabelDevice.h"

class BabelMockDevice: public BabelDevice {
public:
    BabelMockDevice(const char *filename);
    ~BabelMockDevice();
    void begin();
    void read(uint32_t addr, void *data, uint32_t len);
private:
    const char *filename;
    FILE *file;
};

#endif /* BabelMockDevice_h */
