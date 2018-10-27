#!/usr/bin/env python3
# coding: utf-8
from ev3dev.ev3 import *
import Pyro4
import socket

# CLIENTE DO SR

ns = Pyro4.locateNS("192.168.0.14") # IP do PC
uri = ns.lookup('serverSR-SS')
print(uri)
o = Pyro4.Proxy(uri)

class ComunicacaoSR_SS:

    # MOVIMENTO USA ESSA FUNÇÃO
    def setDirecaoManual(self):
         d = o.setDirecao()
         return d


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

