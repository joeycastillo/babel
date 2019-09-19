//
//  BabelSPIFlash.h
//  BabelTest
//
//  Created by Joey Castillo on 9/18/19.
//  Copyright © 2019 Joey Castillo. All rights reserved.
//

#ifndef BabelSPIFlash_h
#define BabelSPIFlash_h

#include <stdio.h>
#include "BabelDevice.h"
#include "Adafruit_SPIFlash.h"

class BabelSPIFlash: public BabelDevice {
public:
    BabelSPIFlash(Adafruit_SPIFlash *flash);
    ~BabelSPIFlash();
    void read(uint32_t addr, void *data, uint32_t len);
private:
    Adafruit_SPIFlash *flash;
};

#endif /* BabelSPIFlash_h */
