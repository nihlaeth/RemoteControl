#!/usr/bin/env python
 
import sys, time, socket, subprocess
from daemon import daemon

port = 64502
clientip = "192.168.1.3"
username = "nihlaeth"
key = "/root/.ssh/arthemis"


def pk(k): #press key
    subprocess.call(["xdotool", "key", k])

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
        pk('super+-')
    elif(c=='workspace-12'):
        pk('super+=')
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
    daemon = MyDaemon('/var/run/RemoteControl.pid')
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






