#!/usr/bin/env python3
# coding: utf-8
import Pyro4
import Pyro4.util

class ClienteSR:
    def setCorLed(self):
        ns = Pyro4.locateNS("10.42.0.79")  # IP do robô
        uri = ns.lookup('ServidorSR')
        print(uri)
        o = Pyro4.Proxy(uri)
        c = input("Informe a cor do led: ")
        cor = int(c)
        print(o.setCorLed(cor))

    def getEndMAC(self):
        ns = Pyro4.locateNS("10.42.0.79")  # IP do robô
        uri = ns.lookup('ServidorSR')
        print(uri)
        o = Pyro4.Proxy(uri)
        print(o.getEndMAC())

    ##acessada via interface gráfica
    def MovimentoManual(self, direcao):
        ns = Pyro4.locateNS("10.42.0.79")  # IP do robô
        uri = ns.lookup('Movimento')
        print(uri)
        try:
            o = Pyro4.Proxy(uri)
            o.move(direcao)
        except Exception:
            print("Pyro traceback:")
            print("".join(Pyro4.util.getPyroTraceback()))

    ##acessada via interface gráfica
    def MovimentoAutonomo(self,):
        print("Iniciando movimento Autônomo")
        ns = Pyro4.locateNS("10.42.0.79")  # IP do robô
        uri = ns.lookup('Movimento')
        print(uri)
        try:
            o = Pyro4.Proxy(uri)
            o.modoJogo(1)
        except Exception:
            print("Pyro traceback:")
            print("".join(Pyro4.util.getPyroTraceback()))