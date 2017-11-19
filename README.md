### Installation
1. Upload multicaptions.ino to your Arduino.

2. Connect your devices as pictured in the diagram below.

3. Starting with a fresh [Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian/) install on your Raspberry Pi, run the following command:

  ```
  sudo raspi-config
  ```
* expand the file system (option #1)
* set the Raspberry Pi to boot to console and turn off the splash screen (option #2)
* enter your locale, timezone, and keyboard layout (option #4)
* finish and reboot

4. Update software:

  ```
  sudo apt-get update
  sudo apt-get dist-upgrade
  ```

5. Install dependencies:
  ```
  sudo apt-get install omxplayer python-dbus python-pip git
  sudo pip install -U srt pyserial
  ```

6. Clone the repository:

  ```
  git clone https://github.com/jasoneppink/multicaptions
  ```
  
7. Change to the multicaptions directory and update config.txt with your details:

  ```
  cd multicaptions
  nano config.txt
  ```
  (Press <kbd>ctrl</kbd>+<kbd>x</kbd>, <kbd>y</kbd>, then <kbd>enter</kbd> to exit and save.)
  
8. Test that your video and subtitles work:

  ```
  python multicaptions.py
  ```

### Bootstrapping
If everything is working, press <kbd>ctrl</kbd>+<kbd>c</kbd> to kill multicaptions.py, then follow these steps to run multicaptions at boot.

1. Make startup.sh executable:

  ```
  chmod 755 startup.sh
  ```
  
2. Open /etc/rc.local:

  ```
  sudo nano /etc/rc.local
  ```
and add this line so multicaptions starts at boot (assuming user and home directory are "pi"):

  ```
  sudo -u pi /home/pi/multicaptions/startup.sh
  ```

3. Reboot! Video will begin to play automatically.

  ```
  sudo reboot
  ```

### Killing multicaptions
If you have multicaptions setup to run on boot and need to stop it for any reason:

1. Connect the Raspberry Pi to a network, reboot it, take note of the IP address, and log in via SSH (assuming user is "pi"):
  ```
  ssh pi@[IP Address]
  ```
  
2. Kill all instances of startup.sh
  ```
  sudo killall startup.sh
  ```


## Wiring

![Wiring](https://github.com/jasoneppink/multicaptions/blob/master/docs/wiring.jpg)

| LCD Display | Arduino |
| ----------- | ------- |
| 1           | GND     |
| 2           | GND     |
| 3           | +5V     |
| 4           | POT terminal 2  |
| 5           | 13      |
| 6           | -       |
| 7           | 12      |
| 8           | 7       |
| 9           | POT terminal 1  |
| 10          | 6       |
| 11          | 11      |
| 12          | 5       |
| 13          | 10      |
| 14          | 4       |
| 15          | 9       |
| 16          | 3       |
| 17          | 8       |
| 18          | 2       |
| 19          | GND     |
| 20          | -       |
