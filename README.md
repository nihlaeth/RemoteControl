RemoteControl
=============

Python module to control a linux pc from a pc with speech recognition installed.

I have a pretty complicated workstation setup, mostly because I'm both a programmer and a person with a disability. I'll try to explain a bit, so you understand what this python module does. I have a (Slackware) linux workstation that I use for about everything. But, I can't type at all without a special typing method called asetniop. I've implemented this for Os X using KeyRemap4MacBook, but haven't managed this for linux yet. I also use speech recognition to give my hands a bit of rest (Dragon for Mac). So I use an Os X pc as a kind of portal to my workstation. Vnc was too slow for my purposes, so I have connected my monitor via a kvm switch, and I port my mouse and keyboard over a ssh tunnel with synergy (this works with asetniop!).

The problem here is that Dragon does not play nice with synergy. I have a lot of custom commands, so I can drive my machines handsfree, but the key events Dragon fires probably skip a few layers, so synergy does not pick up on them. Speech recognition on Linux is not nearly as advanced and accurate as Dragon, so I started searching for a different solution.

I've executed remote commands through ssh (with key authentication) before, but it's slow and I hadn't found a way to fire key events yet. Then I found xdotools and I decided to write a python module that'd send commands over an ssh tunnel, using xdotools & i3-msg (I use i3 as window manager). For security reasons the script only executes a pre-defined set of commands, so if you want to add to it, you'll have to do some coding.

Getting started
============
First of all, you need an ssh key to access the client pc (the one with speech recognition on it) from the server pc (the one you want to control with speech recognition). 

On the server pc:

This will create a key:

    $ ssh-keygen

Follow the on-screen instructions.

Now we'll copy that key over to the client:

    $ ssh-copy-id -i /home/[username]/.ssh/[name-key] [username]@[clientip]

Now we're going to edit the right settings into RemoteControl.py:

    #!/usr/bin/env python 
    ## if env is located somewhere else, edit this path
 
    import sys, time, socket, subprocess
    from daemon import daemon

    port = 64502 ## port that's going to be used by this module
    clientip = "[client ip]"
    username = "[username]" ## username on client pc
    key = "[full path to ssh key]" ## don't use ~ to refer to the home directory, it won't work
    pidfile = "[path to pid file/RemoteControl.pid]" ## some location where you have write privileges, and it won't be in the way

Now start the daemon:
    
    ./RemoteControl.py start

On the client pc:

Copy the RemoteClient.py script over to a conveniet location. Env is not in the same place in linux as it is in os x, so edit the first line as necessary. If you edited the port number in the server script, do so in the client script as well. You are now ready to use the client script. You can put it in /usr/bin to make it system-wide executable, or some other place that's more private. 

Usage:

    /path/to/script/RemoteClient.py command

For a command cheat-sheet, look in the server script. You can now configure your speech recognition to use this script. In dragon for mac, go to tools->commands. Add a new command with global scope. Name it whatever speech pattern you want to use to activate it, and give it type shell script. In the input field, put something like this:

    #!/bin/bash
    /path/to/script/RemoteClient.py workspace-1

Troubleshooting
============

If you get errors of this fashion:

    /usr/bin/env python: No such file or directory

Execute the following command:

    $ which env

And change the first line of the file you were executing to that path, for example:

    #!/bin/env python

If your client throws this error:
    
    Traceback (most recent call last):
      File "./RemoteClient.py", line 9, in <module>
        s.connect(("localhost", 64502))
      File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/socket.py", line 224, in meth
        return getattr(self._sock,name)(*args)
    socket.error: [Errno 61] Connection refused

This most likely means something is wrong with the ssh tunnel. You can check by executing this on the client machine:

    $ telnet localhost 64502

If that says connection refused, the ssh tunnel is not up.

To try if the key is working, go to the server pc and execute this:

    $ ssh -i [path/to/key] [username]@[clientip]

If it asks for a password, try ssh-copy-id again. If it refuses connection, check if your client pc accepts incomming ssh connections (in os x you can turn this on in system preferences->sharing->remote-login).

Another option is that the server process could not create it's pid file in the specified location. You can check this by trying to shut down the server proccess on the server pc:

    $ ./RemoteControl.py stop

If it throws an error, like this:

    pidfile /var/run/RemoteControl.pid does not exist. Daemon not running?

You should probably edit the pid path in the server settings, to a location where you have permissions.

To-Do
============
* close ssh tunnel when shutting down
* add more commands
* include support for domotica through usb-uart / lircd supported hardware
* document commands
* separate settings into config file
* improve error reporting. The daemon library turns this off by default.
