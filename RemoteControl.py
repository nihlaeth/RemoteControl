#!/usr/bin/env python
 
import sys, time, socket
from daemon import daemon
 
class MyDaemon(daemon.Daemon):
    def run(self):
        serve()
 
if __name__ == "__main__":
    daemon = MyDaemon('/var/run/RemoteControl.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
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



def serve():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print "Failed to create socket:", msg
        syst.exit();
    print "Created socket"
    port = 94502
    s.bind(("", port))
    print "Now listening on port", port
    s.listen(10)
    #pynotify.init("Python notification Daemon")
    while 1:
        client, address = s.accept()
        data = client.recv(4096)
        #print "Got connection from", address
        #print data
        control(data)
        #datalist = data.split(":", 1)
        #title = datalist[0]
        #try:
        #    body = datalist[1]
        #except IndexError:
        #    print "No notification body received, using title"
        #    body = title
        #n = pynotify.Notification(title, body)
        #n.show()
        client.close()

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



