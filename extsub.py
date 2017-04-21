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
from langdict import langdict #Language Dictionary
import glob, os
import RPi.GPIO as GPIO
import collections
import serial as s

#output for LCD display - TODO: detect if ttyACM0 or ttyACM1 or something else
ser=s.Serial('/dev/ttyACM1', .9600)

#load serial connection to LCD display
time.sleep(3)

#define "language" and "video"
if(len(sys.argv) > 1):
	language = sys.argv[1]
else:
	language = "eng"

video = "media/test.mp4"

#TODO
#Display "Press Button For Subtitles". When button is pressed, it cycles through the subtitles for one full loop (hitting the end twice)

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

def next_language(channel):
	global subtitles, language, next_i
	j = 0
        while j < len(subtitles):
		if language == subtitles.items()[j][0]:
			if j+1 == len(subtitles):
				language = subtitles.items()[0][0]
			else:
				language = subtitles.items()[j+1][0]
			next_i -= 1
			break
		else:
			j += 1

#setup button
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO21 = pin 40
GPIO.add_event_detect(21, GPIO.FALLING, callback=next_language, bouncetime=200)

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

#import SRT subtitle files into one "subtitles" dict
subtitles = collections.OrderedDict()
os.chdir("media")
for subs in glob.glob("*.srt"):
	lang = subs.split('.')[1]
	with open(subs, 'r') as myfile:
		subfile = myfile.read()
	subtitle_generator = srt.parse(subfile)
	subtitles[lang] = list(subtitle_generator)

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
	start = tc_to_ms(str(subtitles[language][i].start))
	end = tc_to_ms(str(subtitles[language][i].end))
	position = chop_digits(str(dbusIfaceProp.Position()))

	#sys.stdout.write("d: " + duration + " s: " + str(start) + " p: " + str(position) + " e: " + str(end) + " i: " + str(i) + "\n")

	if long(position) > long(start) and long(position) <= long(end):
		if i > next_i:
			next_i += 1
		elif i == next_i:
			#sys.stdout.write(str(subtitles[language][i].content) + "\n")
			ser.write(str(subtitles[language][i].content) + "\r")
			#ser.write(str(subtitles[language][i].content) + "\n")
			#ser.write("test " + str(i) + "\n")
			next_i += 1
	elif long(position) > long(end):
		if subtitles[language][i] == subtitles[language][-1]:
			i = 0
			next_i = 0
			#sys.stdout.write(str(datetime.now()) + "\n")
		else:
			i += 1
	elif long(position) == 0:
		i = 0
		next_i = 0
