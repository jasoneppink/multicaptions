#!/usr/bin/python3
# -*- coding: utf-8 -*-

#sudo apt-get install python3-pip
#sudo apt-get install python3-gi
#sudo apt-get install python3-rpi.gpio
#sudo apt-get install python3-dbus
#sudo pip3 install configparser
#sudo pip3 install pydbus (NO)
#sudo pip3 install srt

#looks like dbus in Python is pydbus in Python3? May need to adjust below
import collections, configparser, datetime, errno, getpass, glob, io, os, pickle, re, srt, subprocess, sys, time, dbus
#from pydbus import SessionBus
from subprocess import Popen
from pprint import pprint
from langdict import langdict #Language Dictionary
import RPi.GPIO as GPIO
from dashboard import update_dashboard

global abs_path, subtitles, sub, language, next_i, write_subtitles, position, sub_start_position, subtitle_duration, played_through_once, launch_state, subtitle_directory, subtitle_image_directory, video, bus, dbusIfaceProp, dbusIfaceKey
global vfd_delay

abs_path = os.path.dirname(os.path.abspath(__file__)) + "/"
vfd_delay = 550 #milliseconds


def tc_to_ms(s): #Converts timecode to milliseconds
    hours, minutes, seconds = (["0", "0"] + s.split(":"))[-3:]
    hours = int(hours)
    minutes = int(minutes)
    seconds = float(seconds)
    ms = int(3600000 * hours + 60000 * minutes + 1000 * seconds) - vfd_delay
    #print(str(ms) + "\n")
    return str(ms)

def chop_digits(s): #Omxplayer's timecode resolution is much higher than SRT files. This chops off the last 3 digits.
    #print(str(s) + "\n")
	if int(s) > 999:
		return s[:-3]
	else:
		return "0"

def initialize():
	global abs_path, subtitles, sub, language, next_i, write_subtitles, position, sub_start_position, subtitle_duration, played_through_once, launch_state, subtitle_directory, subtitle_image_directory, video, bus, dbusIfaceProp, dbusIfaceKey
	#READ CONFIG FILE
	config = configparser.ConfigParser()
	config.readfp(open(abs_path + 'config.txt', 'r'))
	default_lang = config.get('multicaptions config', 'default_lang')
	launch_state = config.get('multicaptions config', 'launch_state')
	video = abs_path + config.get('multicaptions config', 'video_filename')
	print(video + "\n")
	subtitle_directory = abs_path + config.get('multicaptions config', 'subtitle_directory')
	subtitle_image_directory = abs_path + config.get('multicaptions config', 'subtitle_image_directory')
	subtitle_duration = config.get('multicaptions config', 'subtitle_duration')
	#I think I can delete this line:
	#generate_sub_images = config.get('multicaptions config', 'generate_sub_images')

	#initiate assorted variables for tracking subtitle duration
	played_through_once = False
	sub_start_position = ""

	#create/write over .count_plays (number of playthroughs)
	f = open(abs_path + '.count_plays', 'w')
	f.write("0")
	f.close()

	#SET LANGUAGE
	if(len(sys.argv) > 1):
		#first from command line
		language = sys.argv[1]
	else:
		#otherwise from config.txt (default)
		language = default_lang

	write_to_display("init", language, "", 0, 0)
	#write_to_display("sub", language, "NOT USED", 0, 1)

	#SETUP DEFAULT DISPLAY INFO
	if(launch_state == "subtitles"):
		write_subtitles = True
	else:
		write_subtitles = False
		write_to_display("info", language, launch_state)

	#IMPORT SRT FILES
	#store in one "subtitles" dict
	subtitles = collections.OrderedDict()
	os.chdir(subtitle_directory)

	#first add default language
	for subs in glob.glob("*.srt"):
		lang = subs.split('.')[1]
		if(lang == default_lang):
			with io.open(subs, "r", encoding="utf-8-sig") as myfile:
				subfile = myfile.read()
			#print(str(srt.parse(subfile)))
				subtitle_generator = srt.parse(subfile)
				subtitles[lang] = list(subtitle_generator)
			if not os.path.exists(subtitle_image_directory + "/" + lang):
				os.makedirs(subtitle_image_directory + "/" + lang)
			for count, eachsub in enumerate(subtitles[lang]):
				#print(eachsub.content)
				sub = eachsub.content.replace("'", r"\'").encode("utf-8-sig")

	#then add other languages
	for subs in glob.glob("*.srt"):
		lang = subs.split('.')[1]
		with io.open(subs, "r", encoding="utf-8-sig") as myfile:
			subfile = myfile.read()
		subtitle_generator = srt.parse(subfile)
		subtitles[lang] = list(subtitle_generator)

	#SETUP BUTTON
	#this might not detect unless GPIO is made global variable...test...
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO21 = pin 40
	GPIO.add_event_detect(21, GPIO.FALLING, callback=next_language, bouncetime=200)

	#START OMXPLAYER
	#actual command:
	#cmd = "omxplayer -o local --no-osd --loop %s" %(video)
	#for timing debug:
	cmd = "omxplayer -o local --no-osd --loop --subtitle test.eng.srt %s" %(video)
	Popen([cmd], shell=True)

	#START DBUS
	done, retry = 0, 0
	while done==0:
		try:
			with open('/tmp/omxplayerdbus.' + getpass.getuser(), 'r+') as f:
				omxplayerdbus = f.read().strip()
				print(omxplayerdbus)
			bus = dbus.bus.BusConnection(omxplayerdbus)
			object = bus.get_object('org.mpris.MediaPlayer2.omxplayer','/org/mpris/MediaPlayer2', introspect=False)
			dbusIfaceProp = dbus.Interface(object,'org.freedesktop.DBus.Properties')
			print(dbusIfaceProp)
			dbusIfaceKey = dbus.Interface(object,'org.mpris.MediaPlayer2.Player')
			#disable in-player subtitles on video
			#dbusIfaceKey.Action(dbus.Int32("30"))
			done=1
		except:
			retry+=1
			if retry >= 5000:
				print("ERROR")
				raise SystemExit


def next_language(channel):
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
						print("launch stat: " + launch_state + "\n")
						write_subtitles = False
					else:
						write_to_display("info", language, langdict[language].decode("utf-8-sig"))
				else:
					language = subtitles.items()[j+1][0]
					write_to_display("info", language, langdict[language].decode("utf-8-sig"))
				#for debugging language select button, print out date/time and language code
				print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ": " + language + "\n")
				break
			else:
				#keep language the same after first button press
				write_to_display("info", language, langdict[language].decode("utf-8-sig"))
				write_subtitles = True
				break
		else:
			j += 1

def write_to_display(type, lang="", text_to_print="", sub_num=0, sub_num_next=0):
	RAMAddress = sub_num%2 #either 0 or 1
	if type == "info":
		print(type + " " + lang + " " + text_to_print + "\n")
	if type == "init":
		command = abs_path + "vfd/outputvfd new " + lang + " " + str(sub_num) + " " + str(sub_num_next) + " " + str(RAMAddress)
	if type == "sub":
		command = abs_path + "vfd/outputvfd next " + lang + " " + str(sub_num) + " " + str(sub_num_next) + " " + str(RAMAddress)
	print(str(command) + "\n")
	#subprocess.call([command], shell=True)
	Popen([command], shell=True)

def main():
	global abs_path, subtitles, sub, language, next_i, write_subtitles, position, sub_start_position, subtitle_duration, played_through_once, launch_state, subtitle_directory, subtitle_image_directory, video, bus, dbusIfaceProp, dbusIfaceKey
	
	initialize()

	#variables for loop
	i = 0
	next_i = 0
	position = "0"
	duration = "0"

	#write_to_display("init", language)

	#iterate through and print subtitles
	while duration == "0":
		try:
			duration = chop_digits(str(dbusIfaceProp.Duration()))
		except:
			pass

	while int(duration) > int(position):
		start = tc_to_ms(str(subtitles[language][i].start))
		end = tc_to_ms(str(subtitles[language][i].end))
		position = chop_digits(str(dbusIfaceProp.Position()))

		#return to default if subtitle_duration 2 cases are met
		if subtitle_duration == "2" and write_subtitles == True and played_through_once == True and launch_state != "subtitles":
			if int(position) > int(sub_start_position):
				write_subtitles = False
				write_to_display("info", language, launch_state)

		if int(position) > int(start) and int(position) <= int(end):
			#print(str(position) + "\n")
			if i > next_i:
				next_i += 1
			elif i == next_i:
				#requires write_subtitles = True to account for launch_state
				if write_subtitles == True:
					if subtitles[language][i] == subtitles[language][-1]:
						#we're at the last subtitle, so prepare the first one
						write_to_display("sub", language, subtitles[language][i].content, i, 0)
					else:
						write_to_display("sub", language, subtitles[language][i].content, i, i+1)
					print(str(position) + ": " + subtitles[language][i].content + "\n")
				next_i += 1

		elif int(position) > int(end):
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
		elif int(position) == 0:
			i = 0
			next_i = 0

if __name__ == '__main__':
	main()
