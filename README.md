# Raspberry Pi External Subtitles

When museums and galleries who exhibit video attempt to accomodate visitors who are deaf or don't speak the language, they regularly burn hard titles on top of the video image, grossly violating the original work. ([Imagine transcribing a translation directly onto a painting!](https://en.wikipedia.org/wiki/The_Treachery_of_Images))

Inspired by the [New York City Metropolitan Opera's "Met Titles"](http://www.nytimes.com/1995/10/02/arts/reinventing-supertitles-how-the-met-did-it.html?pagewanted=all), Raspberry Pi External Subtitles is a DIY, open source project that uses off-the-shelf hardware to create an affordable, easy-to-build, and easy-to-maintain device that displays a video on a monitor and synchronized subtitles on a separate graphic LCD display.

**This project is still in development.**

##Setup and Installation

1. Configure your Raspberry Pi
Starting with a fresh Raspbian install, use the following command to expand the file system (#1), set the Raspberry Pi to boot to console and turn off the splash screen (#2), and enter your locale, timezone, and keyboard layout (#4). Then finish and reboot.

```
sudo raspi-config
```
2. Update software:

```
sudo apt-get update
sudo apt-get dist-upgrade
```

3. Install dependencies:
```
sudo apt-get install omxplayer python-dbus
sudo pip install -U srt
```

4. Clone the repository:

```
git clone https://github.com/jasoneppink/raspberry-pi-external-subtitles
```

5. Run the application:

```
cd raspberry-pi-external-subtitles
python extsub.py
```

###Dependencies
Raspberry Pi External Subtitles requires [omxplayer](https://github.com/popcornmix/omxplayer), [srt](https://github.com/cdown/srt), and python-dbus. Working with [Rasp-T6963C](https://github.com/Orabig/Rasp-T6963C).

![Mockup](https://github.com/jasoneppink/raspberry-pi-external-subtitles/blob/master/mockup_diagram.jpg)

###Schematic
THIS IS NOT WORKING YET. (Breadboard represents back of [Crystalfontz CFAG24064A graphic LCD display](https://www.crystalfontz.com/products/document/3536/CFAG24064A-TTI-TZ_Datasheet_Release_2016-05-16.pdf).)

![current schematic NOT WORKING YET](https://github.com/jasoneppink/raspberry-pi-external-subtitles/blob/master/schematic.jpg)

###Updates

v0.3 (2016-06-14): Adds support for multiple SRT (subtitle) files. These can be changed immediately by clicking a button that is attached to a pair of GPIO pins. No interface with graphic LCD display yet.

v0.2 (2016-06-06): omxplayer dbus time out problem identified as problem with omxplayer; this is fixed with recent updates to omxplayer (May 27 - June 1, 2016 by kennyyy24 and fabled). This update to raspberry-pi-external-subtitles consolidates dbus calls inside the Python script (eliminating the need for additional bash scripts)

v0.1 (2016-06-01): Synchornization works, but omxplayer dbus times out after 4 hours 38 minutes. No interface with the graphic LCD display yet.
