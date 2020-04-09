#include <stdlib.h>
#include <string.h>

#include "config.h"
#include "Noritake_VFD_GU3000.h"
#include "interface.h"

void Noritake_VFD_GU3000::GU3000_back() {
    command(0x08);
}

void Noritake_VFD_GU3000::GU3000_forward() {
    command(0x09);
}

void Noritake_VFD_GU3000::GU3000_lineFeed() {
    command(0x0a);
}

void Noritake_VFD_GU3000::GU3000_home() {
    command(0x0b);
}

void Noritake_VFD_GU3000::GU3000_carriageReturn() {
    command(0x0d);
}

void Noritake_VFD_GU3000::GU3000_setCursor(unsigned x, unsigned y) {
    command(0x1f);
    command('$');
    command_xy(x, y);
}

void Noritake_VFD_GU3000::GU3000_clearScreen() {
    command(0x0c);
}

void Noritake_VFD_GU3000::GU3000_clearLine() {
    command(0x18);
}

void Noritake_VFD_GU3000::GU3000_clearLineEnd() {
    command(0x019);
}

void Noritake_VFD_GU3000::GU3000_cursorOn() {
    command(0x1f, 'C', 1);
}

void Noritake_VFD_GU3000::GU3000_cursorOff() {
    command(0x1f, 'C', 0);
}

void Noritake_VFD_GU3000::GU3000_init() {
    _delay_ms(NORITAKE_VFD_RESET_DELAY);
    initPort();
    command(0x1b);
    command('@');
}

void Noritake_VFD_GU3000::GU3000_useMultibyteChars(bool enable) {
    us_command('g', 0x02);
    command(enable);
}

void Noritake_VFD_GU3000::GU3000_setMultibyteCharset(uint8_t code) {
    us_command('g', 0x0f);
    command(code);
}

void Noritake_VFD_GU3000::GU3000_useCustomChars(bool enable) {
    command(0x1b, '%', enable);
}

static inline uint8_t getColumn(const uint8_t *src, int col) {
    uint8_t out = 0;
    for (int i=0; i<8; i++)
        if (src[i] & (1<<(4-col))) out += 1<<(7-i);
    return out;
}

void Noritake_VFD_GU3000::GU3000_defineCustomChar(unsigned code, FontFormat format, const uint8_t *data) {
    if (format == _16x16Format || format == _32x32Format) {
        us_command('g', format);
        command(code >> 8);
        command(code);
        print((const char*)data, format==_16x16Format? 32: 128);
        return;
    }
    
    command(0x1b, '&', format & 0xf);
    command(code);
    command(code);
    
    switch (format) {
    case CUUFormat:
        command(5);
        for (uint8_t i=0; i<5; i++)
            command(getColumn(data, i));
        break;
    case _6x8Format:
        command(6);
        print((const char*)data, 6);
        break;
    case _8x16Format:
        command(8);
        print((const char*)data, 16);
        break;
    case _12x24Format:
        command(12);
        print((const char*)data, 36);
        break;
    case _16x32Format:
        command(16);
        print((const char*)data, 64);
        break;
    default: ;
    }
}

void Noritake_VFD_GU3000::GU3000_deleteCustomChar(unsigned code, FontFormat format) {
    if (format == _16x16Format || format == _32x32Format) {
        us_command('g', format+1);
        command(code >> 8);
        command(code);
    } else {
        command(0x01b, '?', format & 0xf);
        command(code);
    }
}

void Noritake_VFD_GU3000::GU3000_setAsciiVariant(AsciiVariant code) {
    if (code < 0x0d)
        command(0x1b, 'R', code);
}

void Noritake_VFD_GU3000::GU3000_setCharset(Charset code) {
    if (code < 0x05 || (0x10 <= code && code <= 0x13))
        command(0x1b, 't', code);
}

void Noritake_VFD_GU3000::GU3000_setScrollMode(ScrollMode mode) {
    command(0x1f);
    command(mode);
}

void Noritake_VFD_GU3000::GU3000_setHorizScrollSpeed(uint8_t speed) {
    command(0x1f, 's', speed);
}

void Noritake_VFD_GU3000::GU3000_invertOff() {
    command(0x1f, 'r', 0);
}

void Noritake_VFD_GU3000::GU3000_invertOn() {
    command(0x1f, 'r', 1);
}

void Noritake_VFD_GU3000::GU3000_setCompositionMode(CompositionMode mode) {
    command(0x1f, 'w', mode);
}

void Noritake_VFD_GU3000::GU3000_setScreenBrightness(unsigned level) {
    if (level <= 100)
        command(0x1f, 'X', 0x10 + (level*10 + 120)/125);
}

void Noritake_VFD_GU3000::GU3000_wait(uint8_t time) {
    us_command('a', 0x01);
    command(time);
}

void Noritake_VFD_GU3000::GU3000_shortWait(uint8_t time) {
    us_command('a', 0x02);
    command(time);
}

void Noritake_VFD_GU3000::GU3000_scrollScreen(unsigned x, unsigned y, unsigned times, uint8_t speed) {
    unsigned pos = (x*NORITAKE_VFD_LINES)+(y/8);
    us_command('a', 0x10);
    command(pos);
    command(pos>>8);
    command(times);
    command(times>>8);
    command(speed);
}

void Noritake_VFD_GU3000::GU3000_wipeScreen(WipeDirection direction, unsigned speed, uint8_t filler) {
    us_command('a', 0x12);
    command(direction);
    command(speed);
    command(filler);
}

void Noritake_VFD_GU3000::GU3000_reverseWipeScreen(WipeDirection direction, unsigned speed, unsigned addr) {
    us_command('a', 0x13);
    command(direction);
    command(speed);
    command(addr);
    command(addr >> 8);
}

void Noritake_VFD_GU3000::GU3000_disolveScreen(unsigned speed, unsigned addr) {
    us_command('a', 0x14);
    command(speed);
    command(addr);
    command(addr >> 8);
}

void Noritake_VFD_GU3000::GU3000_blinkScreen(bool enable, bool reverse, uint8_t onTime, uint8_t offTime, uint8_t times) {
    us_command('a', 0x11);
    command(enable? (reverse? 2: 1): 0);
    command(onTime);
    command(offTime);
    command(times);
}

void Noritake_VFD_GU3000::GU3000_displayOff() {
    us_command('a', 0x40);
    command(0);
}

void Noritake_VFD_GU3000::GU3000_displayOff(uint8_t timer) {
    us_command('a', 0x40);
    command(0x11);
    command(timer);
    us_command('a', 0x40);
    command(0x10);
}

void Noritake_VFD_GU3000::GU3000_displayOn() {
    us_command('a', 0x40);
    command(0x01);
}

void Noritake_VFD_GU3000::GU3000_boldOn() {
    us_command('g', 0x41);
    command(1);
}

void Noritake_VFD_GU3000::GU3000_boldOff() {
    us_command('g', 0x41);
    command(0);
}

void Noritake_VFD_GU3000::GU3000_setFontStyle(FontStyle style) {
    us_command('g', 0x04);
    command(style);
}

void Noritake_VFD_GU3000::GU3000_setFontSize(FontFormat format, uint8_t x, uint8_t y) {
    if (x<=4 && y<=2) {        
        us_command('g', 0x40);
        command(x);
        command(y);
        us_command('g', 0x01);
        command(format);
    }
}

void Noritake_VFD_GU3000::GU3000_selectWindow(uint8_t window) {
    us_command('w', 0x01);
    command(window);
}

void Noritake_VFD_GU3000::GU3000_defineWindow(uint8_t window, unsigned x, unsigned y, unsigned width, unsigned height) {
    us_command('w', 0x02);
    command(window);
    command(0x01);
    command_xy(x, y);
    command_xy(width, height);
}

void Noritake_VFD_GU3000::GU3000_deleteWindow(uint8_t window) {
    us_command('w', 0x02);
    command(window);
    command(0);
    command_xy(0, 0);
    command_xy(0, 0);
}

void Noritake_VFD_GU3000::GU3000_joinScreens() {
    us_command('w', 0x10);
    command(0x01);
}

void Noritake_VFD_GU3000::GU3000_separateScreens() {
    us_command('w', 0x10);
    command(0);
}

void Noritake_VFD_GU3000::print(char c) {
    command(c);
}

void Noritake_VFD_GU3000::print(const char *str) {
    while (*str)
        writePort(*str++);
}

void Noritake_VFD_GU3000::print(const char *buffer, size_t size) {
    while (size--)
        print(*buffer++);
}

void Noritake_VFD_GU3000::print(long number, uint8_t base) {
    if (number < 0) {
        print('-');
        number = -number;
    }
    printNumber(number, base);
}

void Noritake_VFD_GU3000::print(int number, uint8_t base) {
    print((long)number, base);
}

void Noritake_VFD_GU3000::print(unsigned long number, uint8_t base) {
    printNumber(number, base);
}

void Noritake_VFD_GU3000::print(unsigned number, uint8_t base) {
    print((unsigned long)number, base);
}

void Noritake_VFD_GU3000::crlf() {
    GU3000_carriageReturn();
    GU3000_lineFeed();
}

void Noritake_VFD_GU3000::println(char c) {
    print(c);
    crlf();
}

void Noritake_VFD_GU3000::println(const char *str) {
    print(str);
    crlf();
}

void Noritake_VFD_GU3000::println(const char *buffer, size_t size) {
    print(buffer, size);
    crlf();
}

void Noritake_VFD_GU3000::println(long number, uint8_t base) {
    print(number, base);
    crlf();
}

void Noritake_VFD_GU3000::println(int number, uint8_t base) {
    println((long) number, base);
}

void Noritake_VFD_GU3000::println(unsigned long number, uint8_t base) {
    print(number, base);
    crlf();
}

void Noritake_VFD_GU3000::println(unsigned number, uint8_t base) {
    println((unsigned long) number, base);
}

void Noritake_VFD_GU3000::printNumber(unsigned long number, uint8_t base) {
    if (number/base)
        printNumber(number/base, base);
    number %= base;
    print(number + (number < 10? '0': 'A' - 10));
}

void Noritake_VFD_GU3000::GU3000_drawImage(unsigned width, uint8_t height, const uint8_t *data) {
    if (height > NORITAKE_VFD_HEIGHT) return;
    us_command('f', 0x11);
    command_xy(width, height);
    command((uint8_t) 1);
    for (unsigned i = 0; i<(height/8)*width; i++)
        command(data[i]);
}

void Noritake_VFD_GU3000::GU3000_dot(unsigned x, unsigned y, bool on) {
    us_command('d', 0x10);
    command(on);
    command(x);
    command(x>>8);
    command(y);
    command(y>>8);
}
void Noritake_VFD_GU3000::GU3000_shape(Shape shape, unsigned x0, unsigned y0, unsigned x1, unsigned y1, bool on) {
    us_command('d', 0x11);
    command(shape);
    command(on);
    command(x0);
    command(x0>>8);
    command(y0);
    command(y0>>8);
    command(x1);
    command(x1>>8);
    command(y1);
    command(y1>>8);
}

void Noritake_VFD_GU3000::command(uint8_t data) {
    writePort(data);
}
void Noritake_VFD_GU3000::command_xy(unsigned x, unsigned y) {
    command(x);
    command(x>>8);
    y /= 8;
    command(y);
    command(y>>8);
}
void Noritake_VFD_GU3000::command_xy1(unsigned x, unsigned y) {
    command(x);
    command(x>>8);
    command(y);
    command(y>>8);
}

void Noritake_VFD_GU3000::us_command(uint8_t group, uint8_t cmd) {
   command(0x1f);
   command(0x28);
   command(group);
   command(cmd);
}

void Noritake_VFD_GU3000::command(uint8_t prefix, uint8_t group, uint8_t cmd) {
   command(prefix);
   command(group);
   command(cmd);
}

void Noritake_VFD_GU3000::print(unsigned x, uint8_t y, const char *buffer, uint8_t len) {
    us_command('d', 0x30);
    command_xy1(x, y);
    command(0);
    command(len);
    while (len--)
        command(*buffer++);
}

void Noritake_VFD_GU3000::print(unsigned x, uint8_t y, const char *str) {
    print(x, y, str, strlen(str));
}
void Noritake_VFD_GU3000::print(unsigned x, uint8_t y, char c) {
    print(x, y, &c, 1);
}
void Noritake_VFD_GU3000::print(unsigned x, uint8_t y, int number, uint8_t base) {
    if (number < 0) {
        print(x, y, '-');
        print(-1, y, (unsigned)-number, base);        
    } else
        print(x, y, (unsigned)number, base);
}
void Noritake_VFD_GU3000::print(unsigned x, uint8_t y, unsigned number, uint8_t base) {
    char buf[16], *p = buf + sizeof buf;
    do
        *--p = number % base + (number % base < 10? '0': 'A' - 10);
    while (number /= base);
    print(x, y, p, buf + sizeof buf - p);
}
void Noritake_VFD_GU3000::GU3000_drawImage(unsigned x, uint8_t y, unsigned width, uint8_t height, const uint8_t *data) {
    us_command('d', 0x21);
    command_xy1(x, y);
    command_xy1(width, height);
    command(0x01);
    for (unsigned i = 0; i<(height/8)*width; i++)
        command(data[i]);
}
void Noritake_VFD_GU3000::GU3000_drawImage(unsigned x, uint8_t y, ImageMemoryArea area, unsigned long address, uint8_t srcHeight, unsigned width, uint8_t height, unsigned offsetx, unsigned offsety) {
    if (height > NORITAKE_VFD_HEIGHT) return;
    us_command('d', 0x20);
    command_xy1(x, y);
    command(area);
    command(address);
    command(address>>8);
    command(address>>16);
    command(srcHeight/8);
    command(srcHeight/8>>8);
    command_xy1(offsetx, offsety);
    command_xy1(width, height);
    command(0x01);
}

void Noritake_VFD_GU3000::GU3000_drawImage(unsigned x, uint8_t y, ImageMemoryArea area, unsigned long address, unsigned width, uint8_t height) {
    GU3000_drawImage(x, y, area, address, (height + 7) & ~7, width, height, 0, 0);
}

void Noritake_VFD_GU3000::print_p(const char *str) {
    while (pgm_read_byte(str))
        writePort(pgm_read_byte(str++));
}
void Noritake_VFD_GU3000::print_p(unsigned x, uint8_t y, const char *buffer, uint8_t len) {
    us_command('d', 0x30);
    command_xy1(x, y);
    command(0);
    command(len);
    while (len--)
        command(pgm_read_byte(buffer++));
}

void Noritake_VFD_GU3000::print_p(unsigned x, uint8_t y, const char *str) {
    const char *end = str;
    while (pgm_read_byte(end)) end++;
    print_p(x, y, str, end - str);
}

void Noritake_VFD_GU3000::GU3000_drawImage_p(unsigned width, uint8_t height, const uint8_t *data) {
    if (height > NORITAKE_VFD_HEIGHT) return;
    us_command('f', 0x11);
    command_xy(width, height);
    command((uint8_t) 1);
    for (unsigned i = 0; i<(height/8)*width; i++)
        command(pgm_read_byte(data+i));
}

void Noritake_VFD_GU3000::GU3000_drawImage_p(unsigned x, uint8_t y, unsigned width, uint8_t height, const uint8_t *data) {
    us_command('d', 0x21);
    command_xy1(x, y);
    command_xy1(width, height);
    command(0x01);
    for (unsigned i = 0; i<(height/8)*width; i++)
        command(pgm_read_byte(data+i));
}

void Noritake_VFD_GU3000::GU3000_drawImage(ImageMemoryArea area, unsigned long address, uint8_t srcHeight, unsigned width, uint8_t height) {
    if (height > NORITAKE_VFD_HEIGHT) return;
    us_command('f', 0x10);
    command(area);
    command(address);
    command(address>>8);
    command(address>>16);
    command(srcHeight/8);
    command((srcHeight/8)>>8);
    command(width);
    command(width>>8);
    command(height/8);
    command((height/8)>>8);
    command((uint8_t) 1);
}

void Noritake_VFD_GU3000::GU3000_scrollImage(ImageMemoryArea area, unsigned long address, uint8_t srcHeight, unsigned width, uint8_t height, uint8_t speed) {
    if (height > NORITAKE_VFD_HEIGHT) return;
    us_command('f', 0x90);
    command(area);
    command(address);
    command(address>>8);
    command(address>>16);
    command(srcHeight/8);
    command((srcHeight/8)>>8);
    command(width);
    command(width>>8);
    command(height/8);
    command((height/8)>>8);
    command((uint8_t) 1);
    command(speed);
}

void Noritake_VFD_GU3000::GU3000_defineImage(ImageMemoryArea area, unsigned addr, unsigned width, uint8_t height, const uint8_t *data) {
    if (area == RAMImageArea) {
        unsigned size = (height/8)*width;
        us_command('f', 0x01);
        command(addr);
        command(addr >> 8);
        command((uint8_t)0x00); // RAM is only 4KB, extension byte not needed
        command(size);
        command(size >> 8);
        command((uint8_t)0x00); // RAM is only 4KB, extension byte not needed
        while (size--)
            command(*data++);
    }
}

void Noritake_VFD_GU3000::GU3000_defineImage_p(ImageMemoryArea area, unsigned addr, unsigned width, uint8_t height, const uint8_t *data) {
    unsigned size = (height/8)*width;
    us_command('f', 0x01);
    command(addr);
    command(addr >> 8);
    command((uint8_t)0x00); // RAM is only 4KB, extension byte not needed
    command(size);
    command(size >> 8);
    command((uint8_t)0x00); // RAM is only 4KB, extension byte not needed
    while (size--)
        command(pgm_read_byte(data++));
}
