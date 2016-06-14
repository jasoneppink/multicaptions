# Raspberry Pi External Subtitles

Displays subtitles on an external graphic LCD display synchronized to a video.

v0.3 (2016-06-14): Adds support for multiple SRT (subtitle) files. These can be changed immediately but clicking a button that is attached to a pair of GPIO pins. No interface with graphic LCD display yet.

v0.2 (2016-06-06): omxplayer dbus time out problem identified as problem with omxplayer; this is fixed with recent updates to omxplayer (May 27 - June 1, 2016 by kennyyy24 and fabled). This update to raspberry-pi-external-subtitles consolidates dbus calls inside the Python script (eliminating the need for additional bash scripts)

v0.1 (2016-06-01): Synchornization works, but omxplayer dbus times out after 4 hours 38 minutes. No interface with the graphic LCD display yet.
