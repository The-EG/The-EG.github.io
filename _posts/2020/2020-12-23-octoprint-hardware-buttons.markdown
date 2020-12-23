---
layout: post
author: Taylor Talkington
title: Adding Hardware Buttons to Control OctoPrint
date: 2020-12-23 05:17 -0500
---
The saga of getting my Raspberry Pi 4B running OctoPrint and other things smoothly continues...

At this point I've decided to use the touch screen on my *other* RPi, so the RPi4 that runs OctoPrint is now headless. This has seemed to help the WiFi issues and I've gotten it working nicely after trying USB cables...but this also means that canceling a print can't be done while standing at the printer.

My solution:
![hardware buttons](/assets/buttons_1.png)
Physical buttons...with a 3d printed mount and covers, of course.

Now I have a button to cancel the currently running print (red) and reset the wifi (green).

## Wiring ##

The buttons are simple to wire. This setup uses 3 wires for the 2 buttons. One wire from a ground pin to *both* buttons, and then one wire each from a GPIO pin (GPIO 20 & 21) and each button.

## A simple OctoPrint plugin ##

I found the simplest way monitor the GPIO state and control OctoPrint was from an OctoPrint plugin written in Python. There are a couple of plugins that include support for physical buttons, but they also have a ton of features and overhead that I don't need or want.

So, I wrote a very simple one that sets up the GPIO pins with software pull-up resistors, adds callbacks for falling events (when the button is pressed) and then does something when the buttons are pressed:

{% highlight python %}
from __future__ import absolute_import, unicode_literals

import subprocess
import RPi.GPIO as gpio

import octoprint.plugin

class HWButtonsPlugin(octoprint.plugin.SettingsPlugin):
    def __init__(self):
        super().__init__()
        gpio.setmode(gpio.BCM) # use 'GPIO' numbers
        gpio.setup(20, gpio.IN, pull_up_down=gpio.PUD_UP) # green button
        gpio.setup(21, gpio.IN, pull_up_down=gpio.PUD_UP) # red button
        gpio.add_event_detect(20, gpio.FALLING, callback=self.on_button_pressed, bouncetime=1000)
        gpio.add_event_detect(21, gpio.FALLING, callback=self.on_button_pressed, bouncetime=1000)

    def __del__(self):
        gpio.cleanup()

    def on_button_pressed(self, channel):
        if channel==20:
            self._logger.info("Resetting wifi-module. (Hardware button pressed)")
            subprocess.call("/home/taylor/reset_wifi.sh", shell=True)
        if channel==21 and self._printer.is_operational() and self._printer._is_printing() and not self._printer is_cancelling():
            self._logger.info("Cancelling print. (Hardware button pressed)")
            self._printer.cancel_print()

__plugin_name__ = "Hardware Buttons"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Actions for hardware buttons wired to RPi GPIO pins."
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = HWButtonsPlugin()
{% endhighlight %}

Some details:
 - Subclassing `octoprint.plugin.SettingsPlugin` is not used at this point. I plan on making the plugin configuratable at some point...
 - `gpio.setmode(gpio.BCM)` tells `RPi.GPIO` to use the 'GPIO' numbers (ie. GPIO 20) instead of the physical pin numbers.
 - `bouncetime=1000` in the `add_event_detect` calls causes the callback to only be triggered once per second (100 msecs). Otherwise, the callback would be triggered multiple times for a single press due to 'bounce.'
 - All of the `__plugin_*` variables are how OctoPrint reads and loads the plugin

Installing the plugin is simple: place the python file in ~/.ocotprint/plugins and restart OctoPrint.