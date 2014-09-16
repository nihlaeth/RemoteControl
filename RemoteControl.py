#!/usr/bin/env python 
## if env is located somewhere else, change this path
 
import sys, time, socket, subprocess, ConfigParser
from daemon import daemon

config = ConfigParser.ConfigParser()
config.read('config.cfg')

# Set the third, optional argument of get to 1 if you wish to use raw mode.
port = config.get('General', 'port')
clientip = config.get('General', 'clientip')
username = config.get('General', 'username')
key = config.get('General', 'key')
pidfile = config.get('General', 'pidfile')
debug = config.get('General', 'debug')
if(debug=="true" or debug=="1" or debug=="on"): debug = True
else: debug = False
stdin = config.get('General', 'stdin')
stdout = config.get('General', 'stdout')
stderr = config.get('General', 'stderr')

def pk(k): #press key
    subprocess.call(["xdotool", "key", "--clearmodifiers", "--delay", "25", k])

def control(c):
    if(c=='window-up'):
        pk('super+Up')
    elif(c=='window-down'):
        pk('super+Down')
    elif(c=='window-left'):
        pk('super+Left')
    elif(c=='window-right'):
        pk('super+Right')
    elif(c=='workspace-1'):
        pk('super+1')
    elif(c=='workspace-2'):
        pk('super+2')
    elif(c=='workspace-3'):
        pk('super+3')
    elif(c=='workspace-4'):
        pk('super+4')
    elif(c=='workspace-5'):
        pk('super+5')
    elif(c=='workspace-6'):
        pk('super+6')
    elif(c=='workspace-7'):
        pk('super+7')
    elif(c=='workspace-8'):
        pk('super+8')
    elif(c=='workspace-9'):
        pk('super+9')
    elif(c=='workspace-10'):
        pk('super+0')
    elif(c=='workspace-11'):
        pk('super+minus')
    elif(c=='workspace-12'):
        pk('super+equal')
    elif(c=='fullscreen'):
        pk('super+f')
    elif(c=='new-terminal'):
        pk('super+t')
    elif(c=='open-menu'):
        pk('super+m')
    elif(c=='down'):
        pk('Down')
    elif(c=='up'):
        pk('Up')
    elif(c=='left'):
        pk('Left')
    elif(c=='right'):
        pk('Right')
    elif(c=='backspace'):
        pk('Delete')
    elif(c=='enter'):
        pk('Return')
    elif(c=='tab'):
        pk('Tab')
    elif(c=='home'):
        pk('Home')
    elif(c=='end'):
        pk('End')
    elif(c=='detach-screen'):
        pk('Control+a')
        pk('d')
    elif(c=='terminate'):
        pk('Control+c')
    elif(c=='copy'):
        pk('Control+Shift+c')
    elif(c=='paste'):
        pk('Control+Shift+p')
    elif(c=='tw-train'):
        subprocess.call(["xdotool", "key", "--clearmodifiers", "--delay", "25", "Return", "Control+Tab", "Return", "Control+Tab", "Return", "Control+Tab", "Return"])
    elif(c=='ff-new-tab'):
        pk('Control+t')
    elif(c=='ff-back'):
        pk('Control+bracketleft')
    elif(c=='ff-forward'):
        pk('Control+bracketright')
    elif(c=='ff-home'):
        pk('Alt+Home')
    elif(c=='ff-open-file'):
        pk('Control+o')
    elif(c=='ff-reload'):
        pk('Control+r')
    elif(c=='ff-no-cache-reload'):
        pk('Control+Shift+r')
    elif(c=='ff-stop'):
        pk('Esc')
    elif(c=='ff-next-frame'):
        pk('F6')
    elif(c=='ff-prev-frame'):
        pk('Shift+F6')
    elif(c=='ff-print'):
        pk('Control+p')
    elif(c=='ff-save'):
        pk('Control+s')
    elif(c=='ff-zoom-in'):
        pk('Control+plus')
    elif(c=='ff-zoom-out'):
        pk('Control+minus')
    elif(c=='ff-reset-zoom'):
        pk('Control+0')
    elif(c=='ff-copy'):
        pk('Control+c')
    elif(c=='ff-cut'):
        pk('Control+x')
    elif(c=='ff-paste'):
        pk('Control+p')
    elif(c=='ff-paste-plain'):
        pk('Control+Shift+p')
    elif(c=='ff-redo'):
        pk('Control+Shift+z')
    elif(c=='ff-undo'):
        pk('Control+z')
    elif(c=='ff-select-all'):
        pk('Control+a')
    elif(c=='ff-find'):
        pk('Control+f')
    elif(c=='ff-find-next'):
        pk('Control+g')
    elif(c=='ff-find-prev'):
        pk('Control+Shift+g')
    elif(c=='ff-address-bar'):
        pk('Control+j')
    elif(c=='ff-close-tab'):
        pk('Control+w')
    elif(c=='ff-close-window'):
        pk('Control+Shift+w')
    elif(c=='ff-move-tab-left'):
        pk('Control+Shift+Prior')
    elif(c=='ff-move-tab-right'):
        pk('Control+Shift+Next')
    elif(c=='ff-move-tab-start'):
        pk('Control+Home')
    elif(c=='ff-move-tab-end'):
        pk('Control+End')
    elif(c=='ff-new-window'):
        pk('Control+n')
    elif(c=='ff-new-private-window'):
        pk('Control+Shift+p')
    elif(c=='ff-next-tab'):
        pk('Control+Tab')
    elif(c=='ff-prev-tab'):
        pk('Control+Shift+Tab')
    elif(c=='ff-open-in-new-tab'):
        pk('Alt+Return')
    elif(c=='ff-undo-close-tab'):
        pk('Control+Shift+t')
    elif(c=='ff-undo-close-window'):
        pk('Control+Shift+n')
    else:
        pass


def serve():
    subprocess.call(["ssh","-fN", "-R", str(port)+":localhost:"+str(port), "-i", key, username+"@"+clientip])
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        sys.stderr.write("Failed to create socket:" + msg+ '\n')
        sys.exit();
    sys.stdout.write("Created socket\n")
    s.bind(("127.0.0.1", port))
    sys.stdout.write("Now listening on port"+str(port)+'\n')
    s.listen(10)
    while 1:
        client, address = s.accept()
        data = client.recv(4096)
        control(data)
        client.close()




class MyDaemon(daemon.Daemon):
    def run(self):
	sys.stdout.write("running!\n")
        serve()
 
if __name__ == "__main__":
    daemon = MyDaemon(pidfile, debugb=debug, stdin=stdin, stdout=stdout, stderr=stderr)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            sys.stdout.write("Starting...\n")
            daemon.start()
	    sys.stdout.write("Started!\n")
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)






