---
layout: post
author: Taylor Talkington
title: "Running MSVC Command Prompt in Windows Terminal From a Folder"
date: 2020-10-16 08:15 -0400
---

Since I'm stuck on Windows, that also means most of the time I'm using MS Visual Studio 2019 for C/C++ development, or at least the MSVC toolchains that it comes with.

Visual Studio has come a long way in the past few years, and I actually don't mind the community version now, it even works with CMake quite well!

But, there are still times that need or prefer to use the command line, and the environment there hasn't changed in many years. If I open the "x64 Native Tools Command Prompt for VS 2019" shortcut, I'm greet by this ugly thing:
![old terminal](/assets/old_term.png)

Windows 10 has had a [much better terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?activetab=pivot:overviewtab) for a while now. I've actually switch from using ConEMU to it, exclusively.

Unfortunately, it's also a Windows 10 app, and not and old school executable, so configuring and running it requires a different approach.

## Running the VS tools command prompt within Windows Terminal
First thing first, getting the VS 2019 environment to run within Windows Terminal.  
These 'environments' are just batch files that setup the proper paths and environment variables, and this one is no different. I just have to find the batch file that is run...in my case:

{% highlight terminal %}
D:\Programs\VS 2019\VC\Auxiliary\Build\vcvars64.bat
{% endhighlight %}

Telling Windows Terminal to run that is pretty straight forward:
 - Start Windows Terminal
 - Click the down arrow next to the add button on the top of the screen
 - Select Settings
 
This opens settings.json, which houses the configuration for Windows Terminal. To add the MSVC environment, I just need to add a profile to the 'list' array:

{% highlight json %}
{
  "$schema": "https://aka.ms/terminal-profiles-schema",
  "defaultProfile": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
  "profiles":
    {
      "list": [
        {
          "name": "MSVC x64 env",
          "commandline": "%comspec% /K \"\"D:\\Programs\\VS 2019\\VC\\Auxiliary\\Build\\vcvars64.bat\"\"",
          "hidden": false,
          "closeOnExit": true
        },
        ...
      ]
    }
}
{% endhighlight %}

Now Windows Terminal has a 'MSVC x64 env' option under the new/add menu (+ sign).

Good, but this puts me in `C:\Windows\System32` which is never where I want it to be. I want to be able to open this from the context menu in a folder from Windows Explorer instead.

## Running Windows Terminal from an Explorer Context Menu

Adding a command to the context menu in Windows Explorer is fairly easy, but again, Windows Terminal makes things a bit different. Since it's a Windows 10 App, the actual program is in an odd spot.

I found it in the AppData folder:
C:\users\taylo\AppData\Local\Microsoft\WindowsApps\wt.exe

To add the above 'MSVC x64 env' to the context menu when the 'background' of a folder is clicked:
 - Open the Registry Editor
 - Navigate to HKEY_CLASSES_ROOT\Directory\Background\Shell
  - Create the last key, 'Shell', if it doesn't already exist
 - Add a key under Shell, name it something obvious: msvc_x64
 - Change the `(Default)` value to the text of the context menu entry: MSVC x64 Command Prompt Here
 - Add a key under the new one called 'command'
 - Change the `(Default)` value of that key to `"C:\users\taylo\AppData\Local\Microsoft\WindowsApps\wt.exe" -d "%v" -p "MSVC x64 env"`
   Notice the end part, `-p "MSVC x64 env"`, that needs to match the name of the profile defined in settings.json above.
   
 Now I can navigate to a folder, right click and open the MSVC environment there:
 ![context menu](/assets/context_menu.png)
