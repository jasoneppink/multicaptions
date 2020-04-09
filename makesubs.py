#!/usr/bin/python3
# -*- coding: utf-8 -*-

import collections, configparser, io, glob, os, srt, subprocess, sys

def main():
	abs_path = os.path.dirname(os.path.abspath(__file__)) + "/"
	config = configparser.ConfigParser()
	config.readfp(open(abs_path + 'config.txt', 'r'))
	default_lang = config.get('multicaptions config', 'default_lang')
	subtitle_directory = abs_path + config.get('multicaptions config', 'subtitle_directory')
	subtitle_image_directory = abs_path + config.get('multicaptions config', 'subtitle_image_directory')
	generate_sub_images = config.get('multicaptions config', 'generate_sub_images')

	#import SRT subtitle files into one "subtitles" dict
	subtitles = collections.OrderedDict()
	os.chdir(subtitle_directory)

	for subs in glob.glob("*.srt"):
	        lang = subs.split('.')[1]
	        with io.open(subs, "r", encoding="utf-8-sig") as myfile:
	                subfile = myfile.read()
			#sys.stdout.write(str(srt.parse(subfile))) #for debugging
	        subtitle_generator = srt.parse(subfile)
	        subtitles[lang] = list(subtitle_generator)
		if not os.path.exists(subtitle_image_directory + "/" + lang):
			os.makedirs(subtitle_image_directory + "/" + lang)
		for count, eachsub in enumerate(subtitles[lang]):
			#sys.stdout.write(eachsub.content) #for debugging
			sub = eachsub.content.replace("'", r"\'").encode("utf-8-sig")
			cmd = "convert -background black -size 320x64 -density 72 -colors 2 pango:\"<span foreground='white' background='black' font_family='unifont' font_size='16384'>" + sub + "</span>\" -crop 256x64+0+0 +repage " + subtitle_image_directory + "/" + lang + "/" + str(count) + ".bmp"
			# Bitmaps are stored in GNU Unifont 16 pixels high. We use this size to eliminate any resizing or rescaling.
			# It appears Pango's (or IM's?) default DPI is 90, and as a result it is rendering 16pt at 20px.
			# So we have to do a few things to counteract this:
			# 1. Set Pango variable "font_size" to 16pt x 1024, as required by Pango.
			# 2: Set ImageMagick "-density" (DPI) to 72
			# 3: Make the ImageMagick canvas 320 pixels wide (16 characters x 20 pixels) so Pango will render full line.
			# 4: Crop it back to 256x64
			
			subprocess.call([cmd], shell=True)
			sys.stdout.write(cmd + "\n")

if __name__ == '__main__':
	main()
