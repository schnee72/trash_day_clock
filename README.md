My trash is picked up every Thursday, and recycling is picked up every other Thursday. I can never remember, so I put this device together with a Raspberry Pi so that it will turn on a blue LED on trash day, and it will also turn on a green LED when it is recycle day. It accounts for changes to the schedule due to holidays.

It also has a digital display to show the current time, I used an [Adariut 0.56" 4-Digit 7-Segment Display w/12C Backpack](https://www.adafruit.com/product/879). Adafruit has libraries and documentation to easily set it up with Python on a Rasperry Pi, and should work with other similar devices. [Here](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi) is documentation on setting up things up so that thier Circut Python libraries can be used. One thing to note, it is a good idea to install everything with `sudo` so that you can setup `systemd` to autostart the Python script on boot up.

Please note that Python3 is required for this to work, and with the latest versions of Raspberry Pi OS, 3 is the default. Here are the steps I followed at the time of writing this:

`sudo apt update`
`sudo apt upgrade`
`sudo apt install python3-pip`
`sudo pip install --upgrade adafruit-python-shell`
`wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py`
`sudo python raspi-blunka-py`

The specific documentation for setting up the display is found [here](https://learn.adafruit.com/adafruit-led-backpack/0-dot-56-seven-segment-backpack). 

Install the library for the display:

`sudo pip install adafruit-circuitpython-ht16k33`
`sudo apt install python3-pil`

Once the script is up and running on your device, and you want to make it autostart at bootup, copy the `trash_day_clock.service` to `/lib/systemd/system/`. Then do the following:

`sudo systemctl daemon-reload`
`sudo systemctl enable trash_day_clock.service`

Once you reboot, should now start automatically. 

