#include "../src/config.h"
#include "../src/Noritake_VFD_GU3000.h"
Noritake_VFD_GU3000 vfd;

int main() {
  vfd.GU3000_init();
  vfd.GU3000_setFontSize(_8x16Format, 1, 1);
  vfd.print("012345678901234567890123456789012345678901234567890123456789012345678901234567890");
}
