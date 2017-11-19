# Multicaptions

Multicaptions is an open source captioning technology for media installations in museums, galleries, and other public institutions that accommodates opt-in viewing of captions in multiple languages without impinging on the video image.

Running on a Raspberry Pi, Multicaptions displays fullscreen video (up to full HD) while simultaneously processing and displaying subtitles in one or more selectable languages on a separate graphic LCD or VFD display. It is an affordable, easy-to-build, easy-to-maintain, open source project using completely off-the-shelf hardware.

Multicaptions is inspired by [Figaro System's Simultext](http://www.figaro-systems.com/simultextreg.html) (known as ["Met Titles"](http://www.nytimes.com/1995/10/02/arts/reinventing-supertitles-how-the-met-did-it.html?pagewanted=all) at the NYC Metropolitan Opera).

![Sample setup (English)](https://github.com/jasoneppink/multicaptions/blob/master/docs/sample.gif)

## Hardware Requirements
* [Raspberry Pi 2 Model B or above](https://www.adafruit.com/product/3055)
* a monitor and HDMI cable
* cables and components
  * [5V 2.4 Amp power supply](https://www.adafruit.com/product/1995) for the Raspberry Pi
  * [microSD card](https://www.adafruit.com/product/102) for the Raspberry Pi (at least 4GB)
  * [pushbutton](https://www.adafruit.com/product/558) for cycling through languages (optional)
  * [jumper wires](https://www.adafruit.com/product/826) for connecting pushbutton (optional)
* LCD option
  * [Crystalfontz CFAG24064A graphic LCD display](https://www.crystalfontz.com/product/cfag24064attitz-240x64-display-module-graphic)
  * [Arduino Mega 2560](https://www.adafruit.com/product/191)
  * [A to B USB cable](https://www.adafruit.com/product/62) for connecting the Arduino to the Raspberry Pi
  * [10K potentiometer](https://www.adafruit.com/product/562) for setting the LCD display contrast
  * [jumper wires](https://www.adafruit.com/product/826) for connecting Arduino to LCD display
* VFD option
  * [Noritake GU256x64F-3900B Vacuum Fluorescent Display](https://www.noritake-elec.com/products/model?part=GU256X64F-3900B)
  * [RS-232 DE-9 to 7 pin Kit (with 24V power adapter)](http://noritake-vfd.com/sck-ca07pw06-n1.aspx)
  * [USB to RS-232 DB9 Serial Adapter](https://www.amazon.com/Plugable-Adapter-Prolific-PL2303HX-Chipset/dp/B00425S1H8)


## Setup and Installation
See [LCD](https://github.com/jasoneppink/multicaptions/tree/LCD) or [VFD](https://github.com/jasoneppink/multicaptions/tree/VFD) branches for detailed instructions.

## Notes
Multicaptions currently requires that SRT files for the same video have the same number of subtitles with the same start and end times, regardless of language, with a maximum of two lines per subtitle. (e.g. The demo video has 88 subtitles.)

## Thanks
* Big ups to @olikraus for their indispensible [u8g2 library](https://github.com/olikraus/u8g2), without which none of this would be possible.
* Many thanks to Moe Jangda for his work getting the Raspberry Pi to talk to the LCD display.
* High fives to [Sean McIntyre](https://github.com/boxysean) for polishing ("refactoring") my code.
