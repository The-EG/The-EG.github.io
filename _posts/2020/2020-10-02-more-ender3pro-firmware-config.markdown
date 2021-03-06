---
layout: post
author: Taylor Talkington
title: "More Marlin 2.0 Configuration for Ender 3 Pro"
date: 2020-10-02 08:27 -0400
modified_date: 2021-04-09 11:07
tags: 3d-printing
---
*updated 2020-12-02 with current configuration options*

Since [flashing my Ender 3 Pro with Marlin 2.0]({% link _posts/2020/2020-09-19-flashing-ender3-firmware.markdown %}), I've been tweaking things and changing the configuration a bit.

What I've learned:

## Baudrate
Some of the info I've come across suggests upping the baudrate in the firmware from 115200 to 250000. 

I did this, and while the printer can definitely handle it without issues, I think the Raspberry Pi 4 can not. 

My Raspberry Pi 4 has a lot going on, considering everything is going through a single bus at some point:
 - USB serial connection to the Ender 3 Pro
 - USB mouse (touchscreen)
 - USB keyboard
 - HDMI display (touchscreen)
 - Camera (a RaspiCam 1.3), that is in streaming mode for OctoPrint
 - wifi
 
I've had odd, difficult to reproduce issues revolving around wifi, the HDMI display and the camera. Without the display, the wifi would intermittently stop working, or work poorly (huge latency). In some cases, the wifi hardware would crash completely. Sometimes unloading and reloading the kernel module would get it going again, but not always.

This was compounded when I added the touch screen to HDMI port 1: if the camera streaming service was started automatically on bootup, the wifi would never connect. If I manually started the service later, after the wifi was up and working, it all worked, but still had issues.

Using HDMI port 2 seemed to help...on boot, everything started up properly and wifi connected. But, the wifi would still intermittently stop working.

I eventually discovered that the wifi issues seemed to be the worst while I was printing something with OctoPrint, especially since upgrading the firmware. A few times, the wifi stopped working while I was standing at the printer, using the touchscreen.

So, I figured that I'd move the baud rate back to the default and try it.

~~So far, the wifi seems more stable.~~ With more testing, it doesn't appear to have an effect. I guess I'll just increase it back so at least I'm getting better transfer speeds. Back to the drawing board with the RPi 4 wifi!

## Firmware Size
One feature not enabled by default is the 'Filament Change' command. The default firmware that came with the printer had this function and I had used it a few times to create multi-color prints.
I tried doing the same with a normal pause, but it didn't seem to work the same way.

Unfortunately, enabling the command (`ADVANCED_PAUSE_FEATURE` in Configuration_adv.h) adds quite a bit of size to the firmware, and just enabling that caused it to be too large for my 1.1.4 board. Removing the boot screens and other things weren't enough to get the size back down.

Luckily, I found out it's possible to enable some optimizations within the build process that has a significant effect on the firmware's size, and there's already a confiruation with the proper options.

In addition to the compiler optimizations, it also appears that the bootloader I flashed, otpiboot, is a bit smaller than what the default profile expects, so I also get a bit of room back.

This can all be done by using the 'melzi_optimized' environment instead of 'sanguino1284p' in plantofrmio.ini:

{% highlight ini %}
[platformio]
src_dir      = Marlin
boards_dir   = buildroot/share/PlatformIO/boards
default_envs = melzi_optimized
include_dir  = Marlin
{% endhighlight %}


After building, it's now using 94.8% of the available space even with the filament change command enabled...sweet!

## Current configuration
Here's the current config, starting with the Ender 3 Pro configuration in the Marlin examples:

Configuration.h:

{% highlight c++ %}
// That's me!
#define STRING_CONFIG_H_AUTHOR "(Taylor Talkington, Ender-3 Pro)" // Who made the changes.

// disable the Ender bootscreen, save a little space
//#define SHOW_CUSTOM_BOOTSCREEN

// Enable PID bed heating
#define PIDTEMPBED

// 96 for esteps is closer than 93
#define DEFAULT_AXIS_STEPS_PER_UNIT   { 80, 80, 400, 96 }

// Set the default max feedrate to what I normally change it to, especially the extruder
#define DEFAULT_MAX_FEEDRATE { 500, 500, 5, 50}

// A bit more sane values for default max acceleration
#define DEFAULT_MAX_ACCELERATION { 1500, 1500, 100, 5000 }

// Needed to enable the filament change (advanced pause) command
#define NOZZLE_PARK_FEATURE

// Manual mesh bed leveling
#define MESH_BED_LEVELING
// Inset the edges of the manual mesh so that it starts over the leveling screws
#define MESH_INSET 30
// Set the manual mesh through the LCD
#define LCD_BED_LEVELING

// Add a menu item to move between bed corners for manual bed adjustment
#define LEVEL_BED_CORNERS

// Settings to enable better control of 5015 (and other) blower fans at less than 100% speed
#define FAN_SOFT_PWM
#define SOFT_PWM_SCALE 1
#define SOFT_PWM_DITHER

{% endhighlight %}

Configuration_adv.h:

{% highlight c++ %}
// Disable the info menu, save some space
//#define LCD_INFO_MENU

// Show x and y positions in tenths of milimeters when able
#define LCD_DECIMAL_SMALL_XY

// Enable M73 (set progress) command
#define LCD_SET_PROGRESS_MANUALLY

#define SHOW_REMAINING_TIME

#define USE_M73_REMAINING_TIME     // Use remaining time from M73 command instead of estimation
#define ROTATE_PROGRESS_DISPLAY    // Display (P)rogress, (E)lapsed, and (R)emaining time

// Disable to save a little space
//#define SCROLL_LONG_FILENAMES

// Disable to save a LOT of space
//#define ARC_SUPPORT                 // Disable this feature to save ~3226 bytes

// Enable filament change command
#define ADVANCED_PAUSE_FEATURE

// Disable volumetric extrusion (never used anyway)
#define NO_VOLUMETRICS
{% endhighlight %}
