RemoteControl
=============

Python module to control a linux pc from a pc with speech recognition installed.

I have a pretty complicated workstation setup, mostly because I'm both a programmer and a person with a disability. I'll try to explain a bit, so you understand what this python module does. I have a (Slackware) linux workstation that I use for about everything. But, I can't type at all without a special typing method called asetniop. I've implemented this for Os X using KeyRemap4MacBook, but haven't managed this for linux yet. I also use speech recognition to give my hands a bit of rest (Dragon for Mac). So I use an Os X pc as a kind of portal to my workstation. Vnc was too slow for my purposes, so I have connected my monitor via a kvm switch, and I port my mouse and keyboard over a ssh tunnel with synergy (this works with asetniop!).

The problem here is that Dragon does not play nice with synergy. I have a lot of custom commands, so I can drive my machines handsfree, but the key events Dragon fires probably skip a few layers, so synergy does not pick up on them. Speech recognition on Linux is not nearly as advanced and accurate as Dragon, so I started searching for a different solution.

I've executed remote commands through ssh (with key authentication) before, but it's slow and I hadn't found a way to fire key events yet. Then I found xdotools and I decided to write a python module that'd send commands over an ssh tunnel, using xdotools & i3-msg (I use i3 as window manager). For security reasons the script only executes a pre-defined set of commands, so if you want to add to it, you'll have to do some coding.

To-Do
============
* client module
* startup script for ssh tunnel & server
* server module

