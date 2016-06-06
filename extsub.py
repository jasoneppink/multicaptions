#!/usr/bin/python
import re
import subprocess
from subprocess import Popen
import srt
import sys
from pprint import pprint
import time
#from datetime import datetime
import getpass
import dbus

if(len(sys.argv) > 1):
	video = sys.argv[1]
else:
	video = "/home/pi/caption/media/test.mp4"

if(len(sys.argv) > 2):
	subs = sys.argv[2]
else:
	subs = "/home/pi/caption/media/test.srt"

#TODO
#Display "Press Button For Subtitles". When button is pressed, it cycles through the subtitles for one full loop (hitting the end twice)
#Pressing the button cycles through available languages (different SRT files)

#function converts timecode to milliseconds
def tc_to_ms(s):
        hours, minutes, seconds = (["0", "0"] + s.split(":"))[-3:]
        hours = int(hours)
        minutes = int(minutes)
        seconds = float(seconds)
        ms = int(3600000 * hours + 60000 * minutes + 1000 * seconds)
        return str(ms)

#omxplayer's timecode resolution is much higher than SRT files so this chops off the last 3 digits
def chop_digits(s):
        if long(s) > 999:
                return s[:-3]
        else:
                return "0"

#start omxplayer
cmd = "omxplayer --no-osd --loop %s" %(video)
Popen([cmd], shell=True)

#start dbus
done, retry = 0, 0
while done==0:
	try:
		with open('/tmp/omxplayerdbus.' + getpass.getuser(), 'r+') as f:
			omxplayerdbus = f.read().strip()
		bus = dbus.bus.BusConnection(omxplayerdbus)
		object = bus.get_object('org.mpris.MediaPlayer2.omxplayer','/org/mpris/MediaPlayer2', introspect=False)
		dbusIfaceProp = dbus.Interface(object,'org.freedesktop.DBus.Properties')
		dbusIfaceKey = dbus.Interface(object,'org.mpris.MediaPlayer2.Player')
		#disable in-player subtitles on video
		dbusIfaceKey.Action(dbus.Int32("30"))
		done=1
	except:
		retry+=1
		if retry >= 5000:
			print "ERROR"
			raise SystemExit


#import SRT subtitle file as object
with open(subs, 'r') as myfile:
	subfile = myfile.read()
subtitle_generator = srt.parse(subfile)
subtitles = list(subtitle_generator)

#iterate through and print subtitles
i = 0
next_i = 0
position = "0"
duration = "0"
while duration == "0":
	try:
		duration = chop_digits(str(dbusIfaceProp.Duration()))
	except:
		pass

while long(duration) > long(position):
	#sys.stdout.write("position: " + str(position) + "\n")
	start = tc_to_ms(str(subtitles[i].start))
	end = tc_to_ms(str(subtitles[i].end))
	position = chop_digits(str(dbusIfaceProp.Position()))

	#sys.stdout.write("d: " + duration + " s: " + str(start) + " p: " + str(position) + " e: " + str(end) + " i: " + str(i) + "\n")

	if long(position) > long(start) and long(position) <= long(end):
		if i > next_i:
			next_i += 1
		elif i == next_i:
			sys.stdout.write(str(subtitles[i].content) + "\n")
			next_i += 1
	elif long(position) > long(end):
		if subtitles[i] == subtitles[-1]:
			i = 0
			next_i = 0
			#sys.stdout.write(str(datetime.now()) + "\n")
		else:
			i += 1
	elif long(position) == 0:
		i = 0
		next_i = 0
