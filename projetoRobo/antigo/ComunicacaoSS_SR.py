#!/usr/bin/env python3
# coding: utf-8
from ev3dev.ev3 import *
import socket
import Pyro4

# SERVIDOR DO SR

@Pyro4.expose
class ComunicacaoSS_SR:

    def getEndMAC(self):
        mac = ""
        with open('/sys/class/net/bnep0/address', 'r') as f:
            mac = f.readline().rstrip()
        f.close()
        return mac


    def setCorLed(self, cor):
        if cor == 1:
            Leds.set_color(Leds.LEFT, Leds.YELLOW)
            Leds.set_color(Leds.RIGHT, Leds.YELLOW)
        elif cor == 2:
            Leds.set_color(Leds.LEFT, Leds.RED)
            Leds.set_color(Leds.RIGHT, Leds.RED)
        else:
            Leds.set_color(Leds.LEFT, Leds.GREEN)
            Leds.set_color(Leds.RIGHT, Leds.GREEN)
        return "Teste"

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

ns = Pyro4.locateNS(get_ip())
daemon = Pyro4.Daemon(get_ip())
print(get_ip())
uri = daemon.register(ComunicacaoSS_SR)
ns.register('serverSS-SR',uri)
print(uri)
daemon.requestLoop()
