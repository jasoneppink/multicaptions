#!/bin/bash

#clear screen
printf '%b\n' '\033[2J\033[:'
printf 'Acquiring IP address...'
sleep 30s

#print IP address
printf '%b\n' '\033[2J\033[:'
printf 'IP Address: '
ip route get 8.8.8.8 | awk '{print $7; exit}'
sleep 10s

#clear screen again
printf '%b\n' '\033[2J\033[:'

#turn all prompt text black (keeps screen black)
sudo sh -c "TERM=linux setterm -foreground black >/dev/tty0"

#start video playback
while true
do
	/usr/bin/python ${BASH_SOURCE%/*}/extsub.py
done
