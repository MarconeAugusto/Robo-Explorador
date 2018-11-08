#!/usr/bin/env python3
# coding: utf-8

import Pyro4
# Cliente do SS
ns = Pyro4.locateNS("10.42.0.79") # IP do robô
uri = ns.lookup('serverSS-SR')
print(uri)
o = Pyro4.Proxy(uri)

class SupervisorioSS_SR:

    def setCorLed(self):
        c = input("Informe a cor do led: ")
        cor = int(c)
        print(o.setCorLed(cor))

    def getEndMAC(self):
        print(o.getEndMAC())