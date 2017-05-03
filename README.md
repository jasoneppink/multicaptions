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


## Setup
### Installation
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
  
7. Change to the extsub directory and update config.txt with your details:

  ```
  cd extsub
  nano config.txt
  ```
  (Press ctrl-x and y to exit and save.)
  
8. Test that your video and subtitles work:

  ```
  python extsub.py
  ```

### Bootstrapping
If everything is working, press ctrl-c to kill extsub.py, then follow these steps to run extsub at boot.

1. Make startup.sh executable:

  ```
  chmod 755 startup.sh
  ```
  
2. Open /etc/rc.local:

  ```
  sudo nano /etc/rc.local
  ```
and add this line so extsub starts at boot (assuming user and home directory are "pi"):

  ```
  sudo -u pi /home/pi/extsub/startup.sh
  ```

3. Reboot! Video will begin to play automatically.

  ```
  sudo reboot
  ```

### Killing extsub
If you have extsub setup to run on boot and need to stop it for any reason:

1. Connect the Raspberry Pi to a network, reboot it, take note of the IP address, and log in via SSH.

2. Kill all instances of startup.sh
  ```
  sudo killall startup.sh
  ```


## Wiring

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

## Notes
extsub currently requires that SRT files for the same video have the same number of subtitles with the same start and end times, regardless of language, with a maximum of two lines per subtitle. (e.g. The demo video has 88 subtitles.)

## Thanks
* Big ups to @olikraus for their indispensible [u8g2 library](https://github.com/olikraus/u8g2), without which none of this would be possible.
* Many thanks to Moe Jangda for his work getting the Raspberry Pi to talk to the LCD display.
