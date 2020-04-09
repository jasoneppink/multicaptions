#include "config.h"

#if NORITAKE_VFD_INTERFACE==0

#include <stddef.h>
#include <avr/io.h>
#include <util/delay.h>
#include "interface.h"

void initPort() {
    RAISE(OUT);
    DIRECTION(OUT, 1);
    DIRECTION(BUSY, 0);
}

void writePort(uint8_t data) {
    uint8_t i = 1;
    while (CHECK(BUSY));
    LOWER(OUT);
    _delay_us(1e6 / NORITAKE_VFD_BAUD);
    do {
        SETPIN(OUT, data & i);
        _delay_us(1e6 / NORITAKE_VFD_BAUD);
        i+=i;
    } while (i);
    RAISE(OUT);
    _delay_us(1e6 / NORITAKE_VFD_BAUD);
}

#endif
