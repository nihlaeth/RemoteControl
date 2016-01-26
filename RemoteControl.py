#!/usr/bin/env python
# env isn't always at that spot, make sure to check
"""Control a remote computer with speech recognition - server part."""

import sys
import socket
import subprocess
import ConfigParser
from daemon import daemon
from tools.colorlog import log, LOGLEVEL

# pylint: disable=invalid-name
# I hate seeing caps everywhere, I refuse to allcaps my constants!
config = ConfigParser.SafeConfigParser()
config.read('config.cfg')

commands = ConfigParser.SafeConfigParser()
config.read('commands.cfg')

# Set the third, optional argument of get to 1 if you wish to use raw mode.
port = config.get('General', 'port')
clientip = config.get('General', 'clientip')
username = config.get('General', 'username')
key = config.get('General', 'key')
pidfile = config.get('General', 'pidfile')
log_level = config.get('General', 'log_level')
LOGLEVEL.set_level(log_level)

stdin = config.get('General', 'stdin')
stdout = config.get('General', 'stdout')
stderr = config.get('General', 'stderr')


def execute_command(cmd):
    """Fetch key combos from config and execute them."""
    # see if exists in one-press, other wise look at sequence
    # if it's not there at all, throw error!

    # TODO: consider if it's not simpeler to see all commands as sequenses
    keys = []
    try:
        keys.append(config.get('one-press', cmd))
    except ConfigParser.NoOptionError as error:
        try:
            keys.append(config.get('sequence', cmd))
        except ConfigParser.NoOptionError as error:
            log("fail", "Command not found: %s : %s" % (cmd, error))
        else:
            # this is a sequence, so we must fetch the other parts
            i = 2
            while True:
                sequence_cmd = cmd + "-p%d" % i
                try:
                    keys.append(config.get('sequence', sequence_cmd))
                except ConfigParser.NoOptionError as error:
                    break
                else:
                    i += 1
    # Now keys is a list of all key combinations that have to be pressed
    for combo in keys:
        try:
            subprocess.check_call([
                "xdotool",
                "key",
                "--clearmodifiers",
                "--delay",
                "25",
                combo])
        except (OSError, subprocess.CalledProcessError) as error:
            log("fail", "Failed to execute command %s: %s" % (cmd, error))


def serve():
    """Open ssh tunnel and start listening."""
    try:
        subprocess.check_call([
            "ssh",
            "-fN",
            "-R",
            str(port)+":localhost:"+str(port),
            "-i",
            key,
            username+"@"+clientip])
    except (OSError, subprocess.CalledProcessError) as error:
        log("warn", "Failed to open ssh tunnel: %s" % error)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        log("fail", "Failed to create socket:" + msg)
        sys.exit()
    log("info", "Created socket")
    s.bind(("127.0.0.1", int(port)))
    log("info", "Now listening on port"+str(port))
    s.listen(10)
    while True:
        client, _ = s.accept()
        data = client.recv(4096)
        execute_command(data)
        client.close()


class MyDaemon(daemon.Daemon):

    """Daemonize RemoteControl."""

    def run(self):
        """Start the actual process."""
        log("info", "running!")
        serve()

if __name__ == "__main__":
    daemon = MyDaemon(
        pidfile,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            log("info", "Starting...")
            daemon.start()
            log("info", "Started!")
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            log("fail", "Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        log("info", "usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
