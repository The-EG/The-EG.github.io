---
layout: post
author: Taylor Talkington
title: Setting up Tiger VNC Server in Raspberry Pi OS
date: 2022-01-22 16:19EST
---

Raspberry Pi OS comes with RealVNC server already setup, it can be enabled with `sudo rasp-config`. While this is convenient and 'just works' it unfortunately only works well with the RealVNC viewer with the default setup.

Since switching to Linux, I prefer to use TigerVNC viewer, so I either need to fiddle with the realvnc server settings to make it compatible (and only using VNC based authenication, instead of unix users) or I can setup TigerVNC server on the pi too.

## Installation

Installation is straight forward. I want to use the vncserver that runs on top of an actual Xorg display (ie. my RPi's touch screen), and not a virtual one, at least not yet, so I installed just the xorg-extension server:

```terminal
$ sudo apt install tigervnc-xorg-extension
```

## Configuration

With this (mostly undocumented!) extension, it's possible to configure Xorg to also serve as a vncserver without having to run a separate vncserver process.

First, we need to create a xorg configuration file to load the extension in:
```terminal
$ sudo mkdir /etc/X11/xorg.conf.d
$ sudo emacs /etc/X11/xorg.conf.d/10.vnc.conf
```

With the following content:
```config
Section "Module"
  Load "vnc"
EndSection

Section "Screen"
  Identifier "Screen0"
  Option "Desktop" "PrinterPi Touchscreen"
  Option "SecurityTypes" "TLSPlain"
  Option "PlainUsers" "taylor"
EndSection
```
Here's what the options do:
 - `Desktop` gives the vncserver a name, otherwise it's just X11. This is the name displayed in the title of the viewer window.
 - `SecurityTypes` controls how the viewer authenticates. `TLSPlain` means that only an encrypted connection is accepted, and that a username and password from the system are used to verify authenication.
 - `PlainUsers` is a list of users that are allowed to login to this vncserver. Note: they all get the same permissions once logged in, so if a user is logged into the rpi desktop, any action taken will be as that user.

After that, reboot or `sudo systemctl restart lightdm` and you'll be able to connect to the RPi with Tiger vncviewer.
