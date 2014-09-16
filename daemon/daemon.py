#!/usr/bin/env python
 
import sys, os, time, atexit
from signal import SIGTERM
 
class Daemon:
        """
        A generic daemon class.
       
        Usage: subclass the Daemon class and override the run() method
        """
        def __init__(self, pidfile, debugb=False, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
                self.debugb=debug
                self.debug("start init\n")
                self.stdin = stdin
                self.stdout = stdout
                self.stderr = stderr
                self.pidfile = pidfile
                self.debug("stop init\n")
        def debug(self, message):
            """
            do some basic reporting
            """
            if(self.debugb==True):
                sys.stdout.write(message)

        def daemonize(self):
                """
                do the UNIX double-fork magic, see Stevens' "Advanced
                Programming in the UNIX Environment" for details (ISBN 0201563177)
                http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
                """
                self.debug("start daemonize\n")
                try:
                        pid = os.fork()
                        if pid > 0:
                                # exit first parent
                                sys.exit(0)
                except OSError, e:
                        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
                self.debug("split off first fork\n") 
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
                        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
                self.debug("split off second fork\n")
                
                if(self.debugb==True):
                    # redirect standard file descriptors
                    sys.stdout.flush()
                    sys.stderr.flush()
                    si = file(self.stdin, 'r')
                    so = file(self.stdout, 'a+')
                    se = file(self.stderr, 'a+', 0)
                    os.dup2(si.fileno(), sys.stdin.fileno())
                    os.dup2(so.fileno(), sys.stdout.fileno())
                    os.dup2(se.fileno(), sys.stderr.fileno())
                
                self.debug("write pidfile\n")
                # write pidfile
                atexit.register(self.delpid)
                pid = str(os.getpid())
                file(self.pidfile,'w+').write("%s\n" % pid)
                
                self.debug("end daemonize\n")
       
        def delpid(self):
                self.debug("start delpid\n")
                os.remove(self.pidfile)
                self.debug("stop delpid\n")
 
        def start(self):
                """
                Start the daemon
                """
                self.debug("start start\n")
                # Check for a pidfile to see if the daemon already runs
                try:
                        pf = file(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
       
                if pid:
                        message = "pidfile %s already exist. Daemon already running?\n"
                        sys.stderr.write(message % self.pidfile)
                        sys.exit(1)
               
                # Start the daemon
                self.daemonize()
                self.run()
                self.debug("stop start\n")
 
        def stop(self):
                """
                Stop the daemon
                """
                self.debug("start stop\n")
                # Get the pid from the pidfile
                try:
                        pf = file(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
       
                if not pid:
                        message = "pidfile %s does not exist. Daemon not running?\n"
                        sys.stderr.write(message % self.pidfile)
                        return # not an error in a restart
 
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
                self.debug("stop stop\n")
 
        def restart(self):
                """
                Restart the daemon
                """
                self.debug("start restart\n")
                self.stop()
                self.start()
                self.debug("stop restart\n")
 
        def run(self):
                """
                You should override this method when you subclass Daemon. It will be called after the process has been
                daemonized by start() or restart().
                """

