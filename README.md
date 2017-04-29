# External Subtitles for Video Installations (extsub)

External Subtitles for Video Installations (extsub) plays fullscreen video (up to full HD) while simultaneously processing and displaying subtitles in one or more selectable languages on a separate graphic LCD display. It is an affordable (~$150 USD per unit), easy-to-build, easy-to-maintain, open source project using completely off-the-shelf hardware. extsub is inspired by the [New York City Metropolitan Opera's "Met Titles"](http://www.nytimes.com/1995/10/02/arts/reinventing-supertitles-how-the-met-did-it.html?pagewanted=all).

![Sample setup (English)](https://github.com/jasoneppink/extsub/blob/master/docs/sample.gif)

## Hardware Requirements
* [Raspberry Pi 2 Model B or above](https://www.adafruit.com/product/3055)
* [Arduino Mega 2560](https://www.adafruit.com/product/191)
* [Crystalfontz CFAG24064A graphic LCD display](https://www.crystalfontz.com/product/cfag24064attitz-240x64-display-module-graphic)
* a monitor and HDMI cable
* cables and components
  * [5V 2.4 Amp power supply](https://www.adafruit.com/product/1995) for the Raspberry Pi
  * [microSD card](https://www.adafruit.com/product/102) for the Raspberry Pi (at least 4GB)
  * [A to B USB cable](https://www.adafruit.com/product/62) for connecting the Arduino to the Raspberry Pi
  * [jumper wires](https://www.adafruit.com/product/826) for connecting the Arduino to the LCD display
  * [10K potentiometer](https://www.adafruit.com/product/562) for setting the LCD display contrast


## Setup and Installation

1. Upload extsub.ino to your Arduino.

2. Connect your devices as pictured in the diagram below.

3. Starting with a fresh [Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian/) install on your Raspberry Pi, run the following command:

  ```
  sudo raspi-config
  ```
* expand the file system (option #1)
* set the Raspberry Pi to boot to console and turn off the splash screen (option #2)
* enter your locale, timezone, and keyboard layout (option #4)
* finish and reboot

4. Update software:

  ```
  sudo apt-get update
  sudo apt-get dist-upgrade
  ```

5. Install dependencies:
  ```
  sudo apt-get install omxplayer python-dbus python-pip git
  sudo pip install -U srt pyserial
  ```

6. Clone the repository:

  ```
  git clone https://github.com/jasoneppink/extsub
  ```

7. Run the application:

  ```
  cd extsub
  python extsub.py
  ```

### Wiring

![Wiring](https://github.com/jasoneppink/extsub/blob/master/docs/wiring.jpg)

| LCD Display | Arduino |
| ----------- | ------- |
| 1           | GND     |
| 2           | GND     |
| 3           | +5V     |
| 4           | POT terminal 3  |
| 5           | 13      |
| 6           | -       |
| 7           | 12      |
| 8           | 7       |
| 9           | POT terminal 2  |
| 10          | 6       |
| 11          | 11      |
| 12          | 5       |
| 13          | 10      |
| 14          | 4       |
| 15          | 9       |
| 16          | 3       |
| 17          | 8       |
| 18          | 2       |
| 19          | GND     |
| 20          | -       |

### Notes
extsub currently requires that SRT files for the same video have the same number of subtitles with the same start and end times, regardless of language, with a maximum of two lines per subtitle. (e.g. The demo video has 88 subtitles.)

### Updates
v0.6 (2017-04-28): Now has stable language switching via button. (Please note that the subtitles included with the sample are merely rough online translations that are intended to show character support only.)

v0.5 (2017-04-26): Now accomodates Arabic, Chinese, French, Haitian Creole, Russian, and Spanish, as well as English, but currently this must be passed via commandline using the language's three-character ISO code, e.g.:
```
python extsub.py eng
```

v0.4 (2017-04-18): It's working! v0.4 introduces an Arduino Mega 2560, which receives the subtitles as serial data from the Raspberry Pi and uses the [U8g2 library](https://github.com/olikraus/u8g2) to print to the LCD screen. extsub currently only works with English subtitles.

v0.3 (2016-06-14): Adds support for multiple SRT (subtitle) files. These can be changed immediately by clicking a button that is attached to a pair of GPIO pins. No interface with graphic LCD display yet.

v0.2 (2016-06-06): omxplayer dbus time out problem identified as problem with omxplayer; this is fixed with recent updates to omxplayer (May 27 - June 1, 2016 by kennyyy24 and fabled). This update consolidates dbus calls inside the Python script (eliminating the need for additional bash scripts)

v0.1 (2016-06-01): Synchornization works, but omxplayer dbus times out after 4 hours 38 minutes. No interface with the graphic LCD display yet.

### Thanks
Many thanks to Moe Jangda for his work getting the Raspberry Pi to talk to the LCD display.
