## Trash Day Clock

My trash is picked up every Thursday, and recycling is picked up every other Thursday. I can never remember, so I put this device together with a Raspberry Pi so that it will turn on a blue LED on trash day, and it will also turn on a green LED when it is recycle day. It accounts for changes to the schedule due to holidays.

It also has a digital display to show the current time, I used an [Adariut 0.56" 4-Digit 7-Segment Display w/12C Backpack](https://www.adafruit.com/product/879). Adafruit has libraries and documentation to easily set it up with Python on a Rasperry Pi, and should work with other similar devices. [Here](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi) is documentation on setting up things up so that thier Circut Python libraries can be used. One thing to note, it is a good idea to install everything with `sudo` so that you can setup `systemd` to autostart the Python script on boot up.

The specific documentation for setting up the display is found [here](https://learn.adafruit.com/adafruit-led-backpack/0-dot-56-seven-segment-backpack). 

Once the script is up and running on your device, and you want to make it autostart at bootup, copy the `trash_day_clock.service` to `/lib/systemd/system/`. Then do the following:

```
sudo systemctl daemon-reload
```
```
sudo systemctl enable trash_day_clock.service
```

Once you reboot, the script should now start automatically. 

The LEDs I used were 10mm, and had a forward voltage that was either close to the 3.3v default voltage of the Raspberry Pi, or over 3.3v, so I used the 5v output on the Pi to power them. Since the GPIO is 3.3v, I used some NPN transducers to act as a switch to turn the LEDs on and off. This was to prevent damage to the 3.3v GPIO pins on the Pi from the 5v power that was powering the LEDs.

I used the default 3.3v to power the clock display.

![trash_day_clock](https://user-images.githubusercontent.com/13930891/156907942-9959b24c-229d-42d3-a974-23f82d915642.jpg)

