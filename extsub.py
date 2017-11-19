#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import glob, os, errno
import RPi.GPIO as GPIO
import collections
import ConfigParser
from dashboard import update_dashboard
import pickle
import io
from bmp2hex import bmp2hex

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
	global abs_path, subtitles, language, next_i, write_subtitles, position, sub_start_position, subtitle_duration, played_through_once, launch_state
	if(subtitle_duration == "2"):
		sub_start_position = position
		played_through_once = False
	j = 0
        while j < len(subtitles):
		if language == subtitles.items()[j][0]:
			if write_subtitles == True:
				if j+1 == len(subtitles):
					language = subtitles.items()[0][0]
					#revert to default
					if(launch_state != "subtitles"):
						write_to_display("info", language, launch_state)
						sys.stdout.write("launch stat: " + launch_state + "\n")
						write_subtitles = False
					else:
						write_to_display("info", language, langdict[language].decode("utf-8-sig"))
				else:
					language = subtitles.items()[j+1][0]
					write_to_display("info", language, langdict[language].decode("utf-8-sig"))
				#for debugging language select button, print out date/time and language code
				sys.stdout.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ": " + language + "\n")
				break
			else:
				#keep language the same after first button press
				write_to_display("info", language, langdict[language].decode("utf-8-sig"))
				write_subtitles = True
				break
		else:

			j += 1

def write_to_display(type, lang, text_to_print, count=0):
	global subtitle_image_directory
	if type == "info":
		sys.stdout.write(type + " " + lang + " " + text_to_print + "\n")
	if type == "sub":
#		Popen([abs_path + "/Noritake_VFD_GU3000/test/test", type, language, text_to_print])
#		language + str(count) + ".bmp"
#		sys.stdout.write(lang + str(count) + ".bmp\n")
#		temp = bmp2hex(subtitle_image_directory + "/" + lang + "/" + str(count) + ".bmp")
		Popen([abs_path + "/Noritake_VFD_GU3000/imagetest/imagetest", bmp2hex(subtitle_image_directory + "/" + lang + "/" + str(count) + ".bmp")])
def main():
	global abs_path, subtitles, sub, language, next_i, write_subtitles, position, sub_start_position, subtitle_duration, played_through_once, launch_state, subtitle_directory, subtitle_image_directory
	#get absolute path of this script
	abs_path = os.path.dirname(os.path.abspath(__file__)) + "/"

	#read from configuration file
	config = ConfigParser.ConfigParser()
	config.readfp(open(abs_path + 'config.txt', 'r'))
	default_lang = config.get('extsub config', 'default_lang')
	launch_state = config.get('extsub config', 'launch_state')
	video = abs_path + config.get('extsub config', 'video_filename')
	subtitle_directory = abs_path + config.get('extsub config', 'subtitle_directory')
	subtitle_image_directory = abs_path + config.get('extsub config', 'subtitle_image_directory')
	generate_sub_images = config.get('extsub config', 'generate_sub_images')

	#initiate assorted variables for tracking subtitle duration
	subtitle_duration = config.get('extsub config', 'subtitle_duration')
	played_through_once = False
	sub_start_position = ""

	#create/write over .count_plays (number of playthroughs)
	f = open(abs_path + '.count_plays', 'w')
	f.write("0")
	f.close()

	#set language, first from command line, otherwise from config.txt
	if(len(sys.argv) > 1):
		language = sys.argv[1]
	else:
		language = default_lang

	#setup default display info
	if(launch_state == "subtitles"):
		write_subtitles = True
	else:
		write_subtitles = False
		write_to_display("info", language, launch_state)

	#setup button
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO21 = pin 40
	GPIO.add_event_detect(21, GPIO.FALLING, callback=next_language, bouncetime=200)

	#start omxplayer
	cmd = "omxplayer -o local --no-osd --loop %s" %(video)
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

	#first add default language
	for subs in glob.glob("*.srt"):
	        lang = subs.split('.')[1]
		if(lang == default_lang):
		        with io.open(subs, "r", encoding="utf-8-sig") as myfile:
		                subfile = myfile.read()
			#sys.stdout.write(str(srt.parse(subfile)))
		        subtitle_generator = srt.parse(subfile)
		        subtitles[lang] = list(subtitle_generator)
			if not os.path.exists(subtitle_image_directory + "/" + lang):
				os.makedirs(subtitle_image_directory + "/" + lang)
			for count, eachsub in enumerate(subtitles[lang]):
				#sys.stdout.write(eachsub.content)
				sub = eachsub.content.replace("'", r"\'").encode("utf-8-sig")
				cmd = "convert -size 256x64 -fill black -font unifont.tff -pointsize 12 -colors 2 pango:\"" + sub + "\" " + subtitle_image_directory + "/" + lang + "/" + str(count) + ".bmp"
				Popen([cmd], shell=True)
				#sys.stdout.write(cmd + "\n")

	#then add other languages
	for subs in glob.glob("*.srt"):
		lang = subs.split('.')[1]
		with io.open(subs, "r", encoding="utf-8-sig") as myfile:
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
		start = tc_to_ms(str(subtitles[language][i].start))
		end = tc_to_ms(str(subtitles[language][i].end))
		position = chop_digits(str(dbusIfaceProp.Position()))

		#return to default if subtitle_duration 2 cases are met
		if subtitle_duration == "2" and write_subtitles == True and played_through_once == True and launch_state != "subtitles":
			if long(position) > long(sub_start_position):
				write_subtitles = False
				write_to_display("info", language, launch_state)

		if long(position) > long(start) and long(position) <= long(end):
			if i > next_i:
				next_i += 1
			elif i == next_i:
				#requires write_subtitles = True to account for launch_state
				if write_subtitles == True:
					write_to_display("sub", language, subtitles[language][i].content, i)
					#sys.stdout.write(subtitles[language][i].content + "\n")
				next_i += 1
		elif long(position) > long(end):
			if subtitles[language][i] == subtitles[language][-1]:
				i = 0
				next_i = 0
				if launch_state != "subtitles" and write_subtitles == True:
					if(subtitle_duration == "1" or (subtitle_duration == "3" and played_through_once == True)):
						#return display to default state
						write_subtitles = False
						played_through_once = False
						language = default_lang
						write_to_display("info", language, launch_state)
						#ser.write("{DEFAULT" + launch_state + "}")
					elif(subtitle_duration == "3" and played_through_once == False):
						played_through_once = True
					elif(subtitle_duration == "2"):
						played_through_once = True
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

if __name__ == '__main__':
	main()
