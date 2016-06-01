#!/usr/bin/python
import re
import subprocess
from subprocess import Popen
import srt
import sys
from pprint import pprint
import time
from datetime import datetime
import logging

#logging.basicConfig(filename='log.log',level=logging.DEBUG)

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
                return s[:-4]
        else:
                return "0"

			#disable subtitles (if name of video file and SRT file are the same, omxplayer automatically turns them on)
			#dbusIfaceKey.Action(dbus.Int32("30"))
#start omxplayer
cmd = "omxplayer --no-osd --loop %s" %(video)
Popen([cmd], shell=True)

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
		duration = chop_digits(subprocess.check_output(['./get_duration.sh']))
	except:
		pass

while long(duration) > long(position):
	#sys.stdout.write("position: " + str(position) + "\n")
	start = tc_to_ms(str(subtitles[i].start))
	end = tc_to_ms(str(subtitles[i].end))
	position = chop_digits(subprocess.check_output(['./get_position.sh']))

	#sys.stdout.write("d: " + duration + " s: " + str(start) + " p: " + str(position) + " e: " + str(end) + " i: " + str(i) + "\n")

	if long(position) > long(start) and long(position) <= long(end):
		if i > next_i:
			next_i += 1
		elif i == next_i:
			sys.stdout.write(str(subtitles[i].content) + "\n")
			#logging.debug(str(subtitles[i].content))
			next_i += 1
	elif long(position) > long(end):
		if subtitles[i] == subtitles[-1]:
			i = 0
			next_i = 0
			sys.stdout.write(str(datetime.now()) + "\n")
			#logging.debug(str(datetime.now()))
		else:
			i += 1
	elif long(position) == 0:
		i = 0
		next_i = 0
