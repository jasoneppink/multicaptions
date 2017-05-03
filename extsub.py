#!/usr/bin/python

import re
import subprocess
from subprocess import Popen
import srt
import sys
from pprint import pprint
import time
import datetime
import getpass
import dbus
from langdict import langdict #Language Dictionary
import glob, os
import RPi.GPIO as GPIO
import collections
import serial as s
import serial.tools.list_ports
import ConfigParser
from dashboard import update_dashboard

#get absolute path of this script
abs_path = os.path.dirname(os.path.abspath(__file__)) + "/"

#read from configuration file
config = ConfigParser.ConfigParser()
config.readfp(open(abs_path + 'config.txt', 'r'))
default_lang = config.get('extsub config', 'default_lang')
launch_state = config.get('extsub config', 'launch_state')
video = abs_path + config.get('extsub config', 'video_filename')
subtitle_directory = abs_path + config.get('extsub config', 'subtitle_directory')

#create/write over .count_plays (number of playthroughs)
f = open(abs_path + '.count_plays', 'w')
f.write("0")
f.close()

#set up serial connection to Arduino
ports = list(serial.tools.list_ports.comports())
for p in ports:
  if "ACM" in str(p):
    arduino_port = str(p)[:12]
ser=s.Serial(arduino_port, .9600)
time.sleep(3)

#set language, first from command line, otherwise from config.txt
if(len(sys.argv) > 1):
	language = sys.argv[1]
else:
	language = default_lang

#send language to Arduino
ser.write("{" + langdict[language] + language + "}")

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
			#next_i -= 1
			ser.write("{" + langdict[language] + language + "}")
			#for debugging language select button, print out date/time and language code
			sys.stdout.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ": " + language + "\n")
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
os.chdir(subtitle_directory)
for subs in glob.glob("*.srt"):
	lang = subs.split('.')[1]
	with open(subs, 'r') as myfile:
		subfile = myfile.read()
	subtitle_generator = srt.parse(subfile)
	subtitles[lang] = list(subtitle_generator)

#iterate through and print subtitles	
#TODO: different languages may have different number of subtitles. Make the subtitle dependent on duration and now a sequential order (currently i)
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
	start = tc_to_ms(str(subtitles[language][i].start))
	end = tc_to_ms(str(subtitles[language][i].end))
	position = chop_digits(str(dbusIfaceProp.Position()))

	if long(position) > long(start) and long(position) <= long(end):
		if i > next_i:
			next_i += 1
		elif i == next_i:
			ser.write(str(subtitles[language][i].content) + "\r")
			#ser.write(str(subtitles[language][i].content) + "\n")
			next_i += 1
	elif long(position) > long(end):
		if subtitles[language][i] == subtitles[language][-1]:
			i = 0
			next_i = 0
			#update .count_plays (number of playthroughs)
			with open(abs_path + '.count_plays', 'r') as count_video:
				value = int(count_video.read())
			with open(abs_path + '.count_plays', 'w') as count_video:
				count_video.write(str(value + 1))
			#write to /etc/motd
			update_dashboard()
		else:
			i += 1
	elif long(position) == 0:
		i = 0
		next_i = 0
