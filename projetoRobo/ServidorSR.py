#!/usr/bin/env python3
# coding: utf-8
import threading
import time

from ev3dev.ev3 import *
import socket
import Pyro4
from Posicionamento import *

# SERVIDOR DO SR

@Pyro4.expose
class ServidorSR:

    def atualizaPosicao(self, pos, id):
        print("Atualiza pos no SS")
        ns = Pyro4.locateNS("191.36.15.99")  # IP do SS
        uri = ns.lookup('listaCacas')
        self.o = Pyro4.Proxy(uri)

        x = pos.getEixoX()
        y = pos.getEixoY()
        ori = pos.getOrientacao()
        self.o.atualizaPosicaoSS(x,y,ori, id)

    def getEndMAC(self):
        mac = ""
        with open('/sys/class/net/bnep0/address', 'r') as f:
            mac = f.readline().rstrip()
        f.close()
        return mac

    def setCorLed(self, cor):
        if cor == '1':
            Leds.set_color(Leds.LEFT, Leds.YELLOW)
            Leds.set_color(Leds.RIGHT, Leds.YELLOW)
            return 1
        elif cor == '2':
            Leds.set_color(Leds.LEFT, Leds.RED)
            Leds.set_color(Leds.RIGHT, Leds.RED)
            return 2
        elif cor == '3':
            Leds.set_color(Leds.LEFT, Leds.GREEN)
            Leds.set_color(Leds.RIGHT, Leds.GREEN)
            return 3
        elif cor == '4':
            Leds.set_color(Leds.LEFT, Leds.BLACK)
            Leds.set_color(Leds.RIGHT, Leds.BLACK)
            return 4
