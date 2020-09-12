---
layout: post
author: Taylor Talkington
title: "Custom Conky displays through Lua and C++"
date: 2020-09-11 20:20:00 -0400
tags: c++ lua conky
---

![Conky](/assets/brewserver-conky.png)

Working on [Pioneer](https://pioneerspacesim.net/#slide0) again recently inspired me to rewrite much of the code that controls the Brewserver, the Raspberry Pi that controls the fermentation chamber that I use to brew beer.

It was previously all written in Python, because that was quick and easy, but it ended up being terribly interdependent (the thermostat service couldn't start until *after* the database was up and running...) and it really just needed to be torn apart and redone from scratch.

So I did, but this time I wrote much of it in C++. While I do think that was a better choice, that had the unfortunate consequence of breaking the web based interface, still in Python, so I now had no easy way of monitoring what was going on. And, rewriting that would be just as time consuming, if not more, than what I had just done.

I have a monitor connected to the RPi and I noticed while setting up Conky that it is now Lua based and can pull in data from custom Lua scripts. And, from working with Pioneer's 'new' PiGui, I knew that moving data between C(++) and Lua wasn't too difficult either, so I thought Conky would make for a decent solution, at least until I got around to rewriting the web interface.

# Development Environment

The first thing to do was getting the proper development packages. The current version of Raspberry Pi OS, Buster, has multiple versions of Lua available:

{% highlight console %}
taylor@brewserver:~ $ apt search liblua
Sorting... Done
Full Text Search... Done
...
liblua5.1-0/stable 5.1.5-8.1+b1 armhf
...
liblua5.2-0/stable 5.2.4-1.1+b1 armhf
...
liblua5.3-0/stable 5.3.3-1.1 armhf
...
liblua50/stable 5.0.3-8+b1 armhf
...
{% endhighlight %}

To make things worse, changes between 5.1 and 5.2 require breaking changes to code on the C side of things. To keep things simple and to ensure it would be compatible, I used the same version of Lua that Conky was built against:

{% highlight console %}
taylor@brewserver:~ $ apt show conky-std
Package: conky-std
Version: 1.10.8-1
...
Depends: ..., liblua5.1-0, ...
...
{% endhighlight %}

So, Lua 5.1 it is: `sudo apt install liblua5.1-0-dev`

# On the C side

When I rewrote everything in C++, I was somewhat ambitious and thought that I would eventually have multiple executables that do different things, but all needing access to the same data, so I built the bulk of the code into a shared library, libbrewserver.so.

Luckily this made accessing things from Lua even easier, I just needed to write a few functions to export the data I wanted out and I could then load my library as a Lua module:

{% highlight C++ %}
/* luaBS.cpp : Lua Brewserver module */

#include <lua.hpp>

#include "sensor.hpp"
#include "thermostat.hpp"

extern "C" {

using namespace Brewserver;

static int sensor_temp_f(lua_State *L)
{
	const char *name = lua_tostring(L, 1);
	float temp = -1;
	try {
		TemperatureSensorData *s = new TemperatureSensorData(name);
		temp = s->TempF();
		delete s;
	} catch (SharedMemException &ex) {}
	lua_pushnumber(L, temp);
	return 1;
}

...

static const struct luaL_Reg brewserver [] = {
	// Sensor Functions
	{"SensorTempF", sensor_temp_f},
	{"SensorTempC", sensor_temp_c},
	{"SensorLastUpdated", sensor_last_updated},

	// Thermostat Functions
	{"ThermostatGetTargetSensor", thermostat_get_target_sensor},
	{"ThermostatGetLimitSensor", thermostat_get_limit_sensor},
	{"ThermostatGetTargetTemp", thermostat_get_target_temp},
	{"ThermostatGetLimitTemp", thermostat_get_limit_temp},
	{"ThermostatGetMode", thermostat_get_mode},
	{"ThermostatGetStatus", thermostat_get_status},

	{NULL, NULL}
};

int luaopen_brewserver (lua_State *L)
{
	luaL_register(L, "brewserver", brewserver);
	// if I were using Lua 5.2+ I'd need to use the below statement
	// instead of luaL_register
	//luaL_newlib(L, brewserver);
	return 1;
}

} // extern "C"
{% endhighlight %}

It's not pretty, the exception should be handled better, but it's quick and it will work for now.

# CMake

I had also used rewriting the brewserver as an opportunity to learn how to use CMake. But, now I have to get it to link my library against Lua as well. This was surprisingly straight forward once I found the appropriate options.

First, tell CMake I want Lua 5.1:

{% highlight CMake %}
find_package(Lua REQUIRED 5.1)
{% endhighlight %}

Then, if Lua is found, include the new file and appropriate compiler flags:

{% highlight CMake %}
if(LUA_FOUND)
	LIST(APPEND BREWSERVER_SOURCES src/luaBS.cpp)
	LIST(APPEND BREWSERVER_LIBS ${LUA_LIBRARIES})
	LIST(APPEND BREWSERVER_INCS ${LUA_INCLUDE_DIR})
endif(LUA_FOUND)
{% endhighlight %}

This way the library will still build if the Lua dependency isn't met, it just won't have the new Lua export functions included.

# Conky and Lua

Finally, libbrewserver.so can now be loaded as a Lua module, and data can be pulled by calling one of the functions like `sensor_temp_f`, but I still have to tell Conky how to do that.

Conky has a variable called `lua` that will run the specified Lua function, with supplied parameters and then display the returned value. However, this won't handle loading my module and Conky prepends 'conky_' to the function names, so I need a Lua script to load my module and wrap the functions. I also do a bit of formatting on the output too.

{% highlight lua %}
-- conky_brewserver.lua
brewserver = require 'brewserver'

function conky_sensor_temp_f(name)
	return string.format("%.1f°F", brewserver.SensorTempF(name))
end
...
{% endhighlight %}

So now `conky_sensor_temp_f` will call `brewserver.SensorTempF` and format the returned value and the return that back to Conky.

Now I have to tell Conky to load the Lua script:

{% highlight lua %}
-- brewserver.conf - a Conky configuration

conky.config = {
    alignment = 'top_left',
    background = false,
    border_width = 1,
    cpu_avg_samples = 2,
    ...
    lua_load = '/mnt/pidata/home/taylor/conky/conky_brewserver.lua',
    ...
}
...
{% endhighlight %}

And finally use the lua functions:

{% highlight lua %}
...

conky.text = [[
$nodename - Fermentation Chamber

${color grey}Temperature Sensors
$hr
${color grey}Ambient:   $color${lua sensor_temp_f Ambient} ${lua_bar 4 sensor_temp_bar Ambient 30 80}
${color grey}Fermenter: $color${lua sensor_temp_f Fermenter} ${lua_bar 4 sensor_temp_bar Fermenter 30 80}

...
]]
{% endhighlight %}

# Done? Not Quite

The last thing to do is tell Lua where to find libbrewserver.so. If I try to run my new configuration with Conky, I get an error:

{% highlight console %}
taylor@brewserver:~ $ conky --config ~/conky/brewserver.conf
conky: llua_load: /mnt/pidata/home/taylor/conky/conkybrewserver.lua:1: module 'brewserver' not found:
...
{% endhighlight %}

I can do that with an environment variable, `LUA_CPATH`. Note: it's **C**PATH not PATH since this is a shared library, not a lua file:

{% highlight console %}
taylor@brewserver:~ $ LUA_CPATH="/mnt/pidata/brewserver/lib?.so;;" conky --conifg ~/conky/brewserver.conf
conky: desktop window (140011c) is subwindow of root window (389)
conky: window type - normal
conky: drawing to created window (0x1c00001)
conky: drawing to double buffer
...
{% endhighlight %}

Also important to note: it's not just a folder but a pattern, in this case anything begining with 'lib' and has the extension '.so'. Because of that, it needs to be in quotes and use a real path (~ for home won't work). Also, the final ';' at the end causes Lua to still search for other modules using the default paths in addtion to this new one.
