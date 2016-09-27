# Raspberry Pi External Subtitles

When museums and galleries who exhibit video attempt to accomodate visitors who are deaf or don't speak the language, they regularly burn hard titles on top of the video image, grossly violating the original work. ([Imagine transcribing a translation directly onto a painting!](https://en.wikipedia.org/wiki/The_Treachery_of_Images))

Inspired by the [New York City Metropolitan Opera's "Met Titles"](http://www.nytimes.com/1995/10/02/arts/reinventing-supertitles-how-the-met-did-it.html?pagewanted=all), Raspberry Pi External Subtitles is a DIY, open source project that uses off-the-shelf hardware to create an affordable, easy-to-build, and easy-to-maintain device that displays a video on a monitor and synchronized subtitles on a separate graphic LCD display.

Raspberry Pi External Subtitles requires [omxplayer](https://github.com/popcornmix/omxplayer) and [Rasp-T6963C](https://github.com/Orabig/Rasp-T6963C).

**This project is still in development.**

![Mockup](https://github.com/jasoneppink/raspberry-pi-external-subtitles/blob/master/mockup_diagram.jpg)

###Schematic
THIS IS NOT WORKING YET. (Breadboard represents back of [Crystalfontz CFAG24064A graphic LCD display](https://www.crystalfontz.com/products/document/3536/CFAG24064A-TTI-TZ_Datasheet_Release_2016-05-16.pdf).)

![current schematic NOT WORKING YET](https://github.com/jasoneppink/raspberry-pi-external-subtitles/blob/master/schematic.jpg)

###Updates

v0.3 (2016-06-14): Adds support for multiple SRT (subtitle) files. These can be changed immediately by clicking a button that is attached to a pair of GPIO pins. No interface with graphic LCD display yet.

v0.2 (2016-06-06): omxplayer dbus time out problem identified as problem with omxplayer; this is fixed with recent updates to omxplayer (May 27 - June 1, 2016 by kennyyy24 and fabled). This update to raspberry-pi-external-subtitles consolidates dbus calls inside the Python script (eliminating the need for additional bash scripts)

v0.1 (2016-06-01): Synchornization works, but omxplayer dbus times out after 4 hours 38 minutes. No interface with the graphic LCD display yet.
