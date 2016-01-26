#!/usr/bin/env python
"""Daemonize a python process."""

import sys
import os
import time
import atexit
from signal import SIGTERM

from tools.colorlog import log


# pylint: disable=invalid-name,too-many-arguments
# true, naming needs improvement, but idc right now
class Daemon(object):

    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(
            self,
            pidfile,
            stdin='/dev/null',
            stdout='/dev/null',
            stderr='/dev/null'):
        """Save settings."""
        log("info", "Enter init")
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        log("info", "Exit init")

    def daemonize(self):
        """
        Do the UNIX double-fork magic.

        See Stevens' "Advanced Programming in the UNIX Environment"
        for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        log("info", "Enter daemonize")
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            # sys.stderr.write("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
            log(
                "fail",
                "fork #1 failed: %d (%s)" % (e.errno, e.strerror))
            sys.exit(1)
        log("info", "split off first fork")
        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            # sys.stderr.write("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
            log(
                "fail",
                "fork #2 failed: %d (%s)" % (e.errno, e.strerror))
            sys.exit(1)
        log("info", "split off second fork")

        # if not self.debug:
        #    # redirect standard file descriptors
        #    sys.stdout.flush()
        #    sys.stderr.flush()
        #    si = file(self.stdin, 'r')
        #    so = file(self.stdout, 'a+')
        #    se = file(self.stderr, 'a+', 0)
        #    os.dup2(si.fileno(), sys.stdin.fileno())
        #    os.dup2(so.fileno(), sys.stdout.fileno())
        #    os.dup2(se.fileno(), sys.stderr.fileno())

        log("info", "write pidfile")
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s" % pid)
        log("info", "end daemonize")

    def delpid(self):
        """Delete pid file."""
        log("info", "Enter delpid")
        os.remove(self.pidfile)
        log("info", "Exit delpid")

    def start(self):
        """Start the daemon."""
        log("info", "Enter start")
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?"
            # sys.stderr.write(message % self.pidfile)
            log("fail", message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()
        log("info", "Exit start")

    def stop(self):
        """Stop the daemon."""
        log("info", "Enter stop")
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?"
            # sys.stderr.write(message % self.pidfile)
            log("fail", message % self.pidfile)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)
        log("info", "Exit stop")

    def restart(self):
        """Restart the daemon."""
        log("info", "Enter restart")
        self.stop()
        self.start()
        log("info", "Exit restart")

    def run(self):
        """
        You should override this method when you subclass Daemon.

        It will be called after the process has been
        daemonized by start() or restart().
        """
