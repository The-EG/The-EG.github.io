---
layout: post
author: Taylor Talkington
title: Compiling a Custom 'Pristine' Kernel in Debian Linux
date: 2022-01-17 07:15EST
---

I've really been enjoying Linux since coming back to it late last year. To my surprise, almost everything worked or had prebuilt packages: all of my Razer RGB peripherals, NVidia GPU, sound card etc.

The only thing I hadn't gotten working yet was the ASUS Aura RGB headers on my motherboard. Those could be controlled via [OpenRGB](https://openrgb.org), but my particular setup required running a patched kernel. I put this aside for a few months because I figured a custom kernel wouldn't be worth it for something I might use once or twice a year, and I was worried that I'd also have to manually install any dkms built modules I'm using as well, notably my NVidia drivers and OpenRazer.

When I finally did get around to it, I found out that, like many Linux tasks, this is *much* easier than it used to be, and even dkms packages play nicely with a custom kernel when it's built properly.

## Kernerl Sources

One thing that hasn't changed is where to get the sources: [kernel.org](https://kernel.org). Download them, unpack them somewhere convenient and open a new terminal there.

## Applying Patches

Patches can be applied directly to the kenerl source. In my case:
```terminal
$ patch p1 < ~/src/OpenRGB/OpenRGB.patch
```

## Configuration

The current configuration can be used as a base. This will copy the configuration for the currently running Kernel:

``` terminal
$ cp /boot/config-$(uname -r) .config
```

Then make a configuration based on that. Any missing/new values will be prompted. This is the time to select the proper values for anything that might have been added with the patches:
```terminal
$ make oldconfig
```

## Building

This part may take quite a while, but it's easy. Once it's complete there will be several debs in the folder above:
```terminal
$ make deb-pkg -j6
```

## Installing

Installation is just a matter of installing the generated deb packages. Any existing dkms modules will build themselves as needed, GRUB will automatically be updated, etc.
```terminal
$ sudo dpkg -i ../*.deb
```

After that just reboot to use the new kernel!

## Uninstalling old kernels

At this point you likely have 3 or more kernels installed, especially if you do this a few times to update to new kernels. The old versions can be uninstalled.

First, see what versions are installed:
```terminal
$ dpkg --list | grep linux-
```

Then uninstall the packages for the old kernels:
```
$ sudo apt purge linux-headers-5.15.0-2-amd64 linux-headers-5.15.0-2-common linux-image-5.15.0-2-amd64
```

It's a good idea to have the last known good version of the kernel around and probably still the last official Debian built kernel too, so don't uninstall all of them.