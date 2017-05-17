#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, datetime, time, subprocess, ConfigParser

#get absolute path of this script (necessary because it's being called, indirectly, from rc.local)
abs_path = os.path.dirname(os.path.abspath(__file__)) + "/"

#read from configuration file
config = ConfigParser.ConfigParser()
config.readfp(open(abs_path + 'config.txt', 'r'))
video_title = config.get('extsub config', 'video_title')

def get_process_time(output):
	# based on script by Daniel G
	# https://stackoverflow.com/questions/2598145/how-to-retrieve-the-process-start-time-or-uptime-in-python
	try:
		pid = str(int(subprocess.check_output(["pgrep","-of","startup.sh"])))
		proc = subprocess.Popen(['ps','-eo','pid,etime'], stdout=subprocess.PIPE)
		# get data from stdout
		proc.wait()
		results = proc.stdout.readlines()
		# parse data (should only be one)
		for result in results:
			try:
				result.strip()
				if result.split()[0] == pid:
					pidInfo = result.split()[1]
					# stop after the first one we find
					break
			except IndexError:
				pass # ignore it
		else:
			print "Process PID", pid, "doesn't seem to exist!"
			sys.exit(0)
		pidInfo = [result.split()[1] for result in results
			if result.split()[0] == pid][0]
		pidInfo = pidInfo.partition("-")
		if pidInfo[1] == '-':
			# there is a day
			days = int(pidInfo[0])
			rest = pidInfo[2].split(":")
			hours = int(rest[0])
			minutes = int(rest[1])
			seconds = int(rest[2])
		else:
			days = 0
			rest = pidInfo[0].split(":")
			if len(rest) == 3:
				hours = int(rest[0])
				minutes = int(rest[1])
				seconds = int(rest[2])
			elif len(rest) == 2:
				hours = 0
				minutes = int(rest[0])
				seconds = int(rest[1])
			else:
				hours = 0
				minutes = 0
				seconds = int(rest[0])

		if output == "start":
			# get the start time
			secondsSinceStart = days*24*3600 + hours*3600 + minutes*60 + seconds
			# unix time (in seconds) of start
			startTime = time.time() - secondsSinceStart
			# final result
			return datetime.datetime.fromtimestamp(startTime).strftime("%A %B %-d at %-I:%M %p")
		elif output == "duration":
			if days == 1:
				duration = str(days) + " day "
			else:
				duration = str(days) + " days "
			if hours == 1:
				duration += str(hours) + " hour "
			else:
				duration += str(hours) + " hours "
			if minutes == 1:
				duration += str(minutes) + " minute"
			else:
				duration += str(minutes) + " minutes"
			return duration
	except Exception:
		return "n/a (not launched via startup.sh)"

def get_num_plays():
	if os.path.isfile(abs_path + '.count_plays') is True:
                with open(abs_path + '.count_plays') as count_plays:
                        num_plays = count_plays.read()
                return num_plays

def update_dashboard():
	with open('/tmp/motd.tmp', 'w') as dashboard_text:
		dashboard_text.truncate()
		#dashboard_text.write('           _             _     \n')
		#dashboard_text.write('  _____  _| |_ ___ _   _| |__  \n')
		#dashboard_text.write(' / _ \\ \\/ / __/ __| | | | \'_ \\ \n')
		#dashboard_text.write('|  __/>  <| |_\\__ \\ |_| | |_) |\n')
		#dashboard_text.write(' \\___/_/\\_\\\\__|___/\\__,_|_.__/ \n')
		dashboard_text.write('\n')
		dashboard_text.write('Playing: ' + video_title + '\n')
    		dashboard_text.write('Launched: ' + get_process_time("start") + '\n')
		dashboard_text.write('Playing for: ' + get_process_time("duration") + '\n')
		dashboard_text.write('Looped: ' + get_num_plays() + ' times\n\n')
		
	if os.path.isfile('/tmp/motd.tmp'):
		os.system('sudo mv /tmp/motd.tmp /etc/motd')
