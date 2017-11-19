#include "../src/config.h"
#include "../src/Noritake_VFD_GU3000.h"
Noritake_VFD_GU3000 vfd;

int main() {
    vfd.GU3000_init();
    vfd.print("Noritake");
    for (;;)
        // go from 0% - 100% in 9 steps
        for (int i = 0; i <= 8; i++) {
            int percent = i * 125 / 10;
            vfd.GU3000_setScreenBrightness(percent);
            vfd.GU3000_setCursor(0, 8);
            vfd.print(percent, 10);
            vfd.print("% Brightness");
            _delay_ms(1000);
        }
}
