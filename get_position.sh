#!/bin/bash

#set -x

OMXPLAYER_DBUS_ADDR="/tmp/omxplayerdbus.${USER:-root}"
OMXPLAYER_DBUS_PID="/tmp/omxplayerdbus.${USER:-root}.pid"
export DBUS_SESSION_BUS_ADDRESS=`cat $OMXPLAYER_DBUS_ADDR`
export DBUS_SESSION_BUS_PID=`cat $OMXPLAYER_DBUS_PID`

[ -z "$DBUS_SESSION_BUS_ADDRESS" ] && { echo "Must have DBUS_SESSION_BUS_ADDRESS" >&2; exit 1; }

position=`DBUS_VERBOSE=1 dbus-send --print-reply=literal --session --reply-timeout=500 --dest=org.mpris.MediaPlayer2.omxplayer /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Position`
#[ $? -ne 0 ] && exit 1
[ $? -eq 0 ] && position="$(awk '{print $2}' <<< "$position")"
if [ ! -z $position ]; then
	echo $position
else
	echo "0"
	#echo "0000"
fi
