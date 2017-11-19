#!/usr/bin/env python

# A script for converting a 1-bit bitmap to HEX for use by Noritake GU3000 series VFD displays
# Based on bmp2hex.py by Robert Gallup, 2016 

import sys, array, os, textwrap, math, random, argparse

# Utility function. Return a long int from array (little endian)
def getLONG(a, n):
	return (a[n+3] * (2**24)) + (a[n+2] * (2**16)) + (a[n+1] * (2**8)) + (a[n])

# Main conversion function
def bmp2hex(infile):

	# Open File
	fin = open(os.path.expanduser(infile), "rb")
	uint8_tstoread = os.path.getsize(os.path.expanduser(infile))
	valuesfromfile = array.array('B')
	try:
		valuesfromfile.fromfile(fin, uint8_tstoread)
	finally:
		fin.close()

        binary_image = ''
        k=0

	# Get bytes from file
        values=valuesfromfile.tolist()

        # Calculate and print pixel size
        pixelWidth  = getLONG(values, 18)
        pixelHeight = getLONG(values, 22)
        #print pixelWidth, pixelHeight

	# Create lists of lists that corresponds to display resolution
	w, h = pixelWidth, pixelHeight;
	Matrix = [[0 for x in range(h)] for y in range(w)] 

	# Isolate and output binary into one long string
	for i in range (146, len(values)):
#	for i in range (62, len(values)-2):
		binary_image += bin(values[i]).lstrip('-0b').zfill(8)

	# separate each bit into matrix
	for j in range (pixelHeight-1, -1, -1): #horizonal mirror b/c BMPs are built from the bottom up
		for i in range (0, pixelWidth):
			Matrix[i][j] = binary_image[k]
			k+=1

	# print matrix - easy visual check on the command line
#	for j in range (0, pixelHeight):
#		for i in range (0, pixelWidth):
#			sys.stdout.write(Matrix[i][j])
#		sys.stdout.write("\n")

	# convert to hex, 8 bits at a time in column order (top to bottom, left to right)
	column_order_byte = ''
	output_string = ''
	for i in range (0, pixelWidth):
		for j in range (0, pixelHeight):
			column_order_byte += Matrix[i][j]
			if len(column_order_byte) == 8:
				inverted_column_order_byte = ''.join('1' if x == '0' else '0' for x in column_order_byte)
				output_string = output_string + hex(int(inverted_column_order_byte, 2)) + ", "
				column_order_byte = ''
				inverted_column_order_byte = ''
	return output_string
