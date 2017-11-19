****************************************************************
                        GU-3000 BRIGHTNESS DEMO
****************************************************************
YOU MUST AGREE THIS TERMS AND CONDITIONS. THIS SOFTWARE IS
PROVIDED BY NORITAKE CO., INC "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR SORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

----------------------------------------------------------------
ABOUT THIS DEMO
This project demonstrates how to use the Noritake_VFD_GU3000
code library to change the brightness of the screen on the
Noritake GU-3000 Vacuum Fluorescent Display (VFD) modules.
You MUST download and install the Noritake_VFD_GU3000 code
library before running the demo.

    http://www.noritake-elec.com

Please refer to the instructions on the download page and
"README" included with the Noritake_VFD_GU3000 code library for
information on how to install the Noritake_VFD_GU3000 code
library and demos.  This document assumes that you have already
configured the "config.h" file in the Noritake_VFD_GU3000 code
library as described in those documents.

For more information on the methods used in this document,
please refer to the method documentation in the
Noritake_VFD_GU3000 code library.

----------------------------------------------------------------
KEY POINTS
1) initialize the module with GU3000_init().
2) Use GU3000_setScreenBrightness() to set the screen brightness
   as a percentage from 0% - 100%: 0% turns the screen off;
   100% turns the screen to its maximum brightness.
3) Though the value is given as a percentage, the display only
   has 8 levels of brightness:
    13%, 25%, 38%, 50%, 63%, 75%, 88%, and 100%
   Any percent other than these is rounded up to the next
   possible level.

----------------------------------------------------------------
LISTING
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



----------------------------------------------------------------
E-M-0133-00 09/13/2012
----------------------------------------------------------------
SUPPORT

For further support, please contact:
    Noritake Co., Inc.
    2635 Clearbrook Dr 
    Arlington Heights, IL 60005 
    800-779-5846 
    847-439-9020
    support.ele@noritake.com

All rights reserved. © Noritake Co., Inc.