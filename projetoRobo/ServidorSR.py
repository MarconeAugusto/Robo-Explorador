#!/usr/bin/env python3
# coding: utf-8
import threading
import time

from ev3dev.ev3 import *
import socket
import Pyro4

# SERVIDOR DO SR

@Pyro4.expose
class ServidorSR:

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
