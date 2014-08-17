#!/bin/env python



import socket
import sys
message = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 5757)) #seshata
s.send(message)
s.close()
