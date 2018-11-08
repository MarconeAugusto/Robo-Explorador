#!/usr/bin/env python3
# coding: utf-8
import Pyro4
import socket
from InterfaceGrafica import *

# SERVIDOR DO SS

@Pyro4.expose
class SupervisorioSR_SS:

    def setDirecao(self):
        raiz = Tk()
        grafico = InterfaceGrafica(raiz)
        return grafico.desenhar()

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
uri = daemon.register(SupervisorioSR_SS)
ns.register('serverSR-SS',uri)
print(uri)
daemon.requestLoop()