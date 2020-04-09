#include <stdint.h>
#include <stddef.h>


enum Shape {
    LineShape = 0,
    HollowRectShape = 1,
    FilledRectShape = 2
};

enum ImageMemoryArea {
    RAMImageArea = 0,
    FlashImageArea = 1,
    ScreenImageArea = 2
};

enum WipeDirection {
    RightToLeft = 0x00,
    LeftToRight = 0x01,
    OpenCurtain = 0x02,
    CloseCurtain = 0x03
};

enum ScrollMode {
    WrappingMode =    1,
    VertScrollMode =  2,
    HorizScrollMode = 3,
    RightAlignScrollMode = 5
};

enum CompositionMode {
    NormalCompositionMode = 0,
    OrCompositionMode =     1,
    AndCompositionMode =    2,
    XorCompositionMode =    3
};

enum FontStyle {
    FixedFont = 0,
    ProportionalFont1 = 2,
    ProportionalFont2 = 3,
    ProportionalFont3 = 4,
};
enum FontFormat {
     _6x8Format = 1,
     CUUFormat =    0x81,
     LCDFormat =    CUUFormat,
     _8x16Format = 2,
     _12x24Format = 3,
     _16x32Format = 4,
     _16x16Format = 0x10,
     _32x32Format = 0x14
};
enum CustomCharacter {
    CustomJapanese = 0xec40,
    CustomKorean = 0xfea1,
    CustomSimplified = 0xfea1,
    CustomTraditional = 0xfea1
};
enum AsciiVariant {
    AmericaAscii =  0,
    FranceAscii =   1,
    GermanyAscii =  2,
    EnglandAscii =  3,
    Denmark1Ascii = 4,
    SweedenAscii =  5,
    ItalyAscii =    6,
    Spain1Ascii =   7,
    JapanAscii =    8,
    NorwayAscii =   9,
    Denmark2Ascii = 10,
    Spain2Ascii =   11,
    LatinAmericaAscii = 12,
    KoreaAscii = 13
};
enum Charset {
    CP437 = 0, EuroStdCharset = CP437,
    Katakana = 1,
    CP850 = 2, MultilingualCharset = CP850,
    CP860 = 3, PortugeseCharset = CP860,
    CP863 = 4, CanadianFrenchCharset = CP863,
    CP865 = 5, NordicCharset = CP865,
    CP1252 = 0x10,
    CP866 = 0x11, Cyrillic2Charset = CP866,
    CP852 = 0x12, Latin2Charset = CP852,
    CP858 = 0x13
};
enum MultibyteCharset {
    ShiftJIS = 0, JapaneseMBCS = ShiftJIS,      // JIS (X0208 Shift-JIS)
    KSC5601 = 1, KoreanMBCS = KSC5601,          // KSC5601-87
    GB2312 = 2, SimplifiedChineseMBCS = GB2312, // GB2312-80
    Big5 = 3, TraditionalChineseMBCS = Big5     // Big5
};

class Noritake_VFD_GU3000 {

    void initialState();
    void printNumber(unsigned long number, uint8_t base);
    void printNumber(unsigned x, uint8_t y, unsigned long number, uint8_t base);
    void command(uint8_t data);
    void us_command(uint8_t group, uint8_t cmd);
    void command(uint8_t prefix, uint8_t group, uint8_t cmd);
    void command_xy(unsigned x, unsigned y);
    void command_xy1(unsigned x, unsigned y);
    void crlf();

public:
    void print(char c);
    void print(const char *str);
    void print(const char *buffer, size_t size);
    void print(int number, uint8_t base);
    void print(unsigned number, uint8_t base);
    void print(long number, uint8_t base);
    void print(unsigned long number, uint8_t base);
    void println(char c);
    void println(const char *str);
    void println(const char *buffer, size_t size);
    void println(int number, uint8_t base);
    void println(unsigned number, uint8_t base);
    void println(long number, uint8_t base);
    void println(unsigned long number, uint8_t base);
    void GU3000_back();
    void GU3000_forward();
    void GU3000_lineFeed();
    void GU3000_home();
    void GU3000_carriageReturn();
    void GU3000_setCursor(unsigned x, unsigned y);
    void GU3000_clearScreen();
    void GU3000_clearLine();
    void GU3000_clearLineEnd();
    void GU3000_cursorOn();
    void GU3000_cursorOff();
    void GU3000_setFontStyle(FontStyle style);
    void GU3000_setFontSize(FontFormat format, uint8_t x, uint8_t y);
    void GU3000_boldOn();
    void GU3000_boldOff();
    void GU3000_init();
    void GU3000_useMultibyteChars(bool enable);
    void GU3000_setMultibyteCharset(uint8_t code);
    void GU3000_useCustomChars(bool enable);
    void GU3000_defineCustomChar(unsigned code, FontFormat format, const uint8_t *data);
    void GU3000_deleteCustomChar(unsigned code, FontFormat format);
    void GU3000_setAsciiVariant(AsciiVariant code);
    void GU3000_setCharset(Charset code);
    void GU3000_setScrollMode(ScrollMode mode);
    void GU3000_setHorizScrollSpeed(uint8_t speed);
    void GU3000_invertOn();
    void GU3000_invertOff();
    void GU3000_setCompositionMode(CompositionMode mode);
    void GU3000_setScreenBrightness(unsigned level);
    void GU3000_wait(uint8_t time);
    void GU3000_shortWait(uint8_t time);
    void GU3000_scrollScreen(unsigned x, unsigned y, unsigned count, uint8_t speed);
    void GU3000_blinkScreen(bool enable, bool reverse, uint8_t on, uint8_t off, uint8_t times);
    void GU3000_displayOn();
    void GU3000_displayOff();
    void GU3000_displayOff(uint8_t timer);
    void GU3000_wipeScreen(WipeDirection direction, unsigned speed, uint8_t filler);
    void GU3000_reverseWipeScreen(WipeDirection direction, unsigned speed, unsigned addr);
    void GU3000_disolveScreen(unsigned speed, unsigned addr);
    void GU3000_drawImage(unsigned width, uint8_t height, const uint8_t *data);
    void GU3000_drawImage_p(unsigned width, uint8_t height, const uint8_t *data);
    void GU3000_drawImage(ImageMemoryArea area, unsigned long address, uint8_t srcHeight, unsigned width, uint8_t height);
    void GU3000_drawImage(unsigned x, uint8_t y, ImageMemoryArea area, unsigned long address, uint8_t srcHeight, unsigned width, uint8_t height, unsigned offsetx, unsigned offsety);
    void GU3000_drawImage(unsigned x, uint8_t y, ImageMemoryArea area, unsigned long address, unsigned width, uint8_t height);
    void GU3000_drawImage_p(unsigned x, uint8_t y, unsigned width, uint8_t height, const uint8_t *data);
    void GU3000_drawImage(unsigned x, uint8_t y, unsigned width, uint8_t height, const uint8_t *data);
    void print(unsigned x, uint8_t y, char c);
    void print(unsigned x, uint8_t y, const char *str);
    void print(unsigned x, uint8_t y, const char *buffer, uint8_t len);
    void print(unsigned x, uint8_t y, int number, uint8_t base);
    void print(unsigned x, uint8_t y, unsigned number, uint8_t base);
    void print_p(const char *str);
    void print_p(unsigned x, uint8_t y, const char *str);
    void print_p(unsigned x, uint8_t y, const char *buffer, uint8_t len);
    void GU3000_defineImage(ImageMemoryArea area, unsigned addr, unsigned width, uint8_t height, const uint8_t *data);
    void GU3000_defineImage_p(ImageMemoryArea area, unsigned addr, unsigned width, uint8_t height, const uint8_t *data);
    void GU3000_scrollImage(ImageMemoryArea area, unsigned long address, uint8_t srcHeight, unsigned width, uint8_t height, uint8_t speed);
    void GU3000_selectWindow(uint8_t window);
    void GU3000_defineWindow(uint8_t window, unsigned x, unsigned y, unsigned width, unsigned height);
    void GU3000_deleteWindow(uint8_t window);
    void GU3000_joinScreens();
    void GU3000_separateScreens();
    void GU3000_dot(unsigned x, unsigned y, bool on=true);
    void GU3000_shape(Shape shape, unsigned x0, unsigned y0, unsigned x1, unsigned y1, bool on=true);
};
