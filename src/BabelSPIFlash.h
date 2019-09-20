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
#include "SPI.h"
#include "BabelDevice.h"

class BabelSPIFlash: public BabelDevice {
public:
    BabelSPIFlash(uint8_t ss, SPIClass *spi);
    void begin();
    void read(uint32_t addr, void *data, uint32_t len);
private:
    uint8_t cs;
    SPIClass *spi;
    SPISettings settings;

    void read(uint32_t addr, uint8_t *data, uint32_t len);
    bool runCommand(uint8_t command);
    bool readCommand(uint8_t command, uint8_t* response, uint32_t len);
    uint8_t readStatus();
    uint8_t readStatus2(void);
};

#endif /* BabelSPIFlash_h */
