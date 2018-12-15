#!/usr/bin/env python3
# coding: utf-8

import subprocess
import threading
import time
import Pyro4
import socket
from time import sleep
from Movimento import *
from ServidorSR import *

########################################################################################################################
class Controle(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def get_ip(self):
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

    def startServer(self):
        print("start server")
        Ip = Controle.get_ip(self)
        str = "pyro4-ns --host "
        cmd = str + Ip
        print(cmd)
        subprocess.call(cmd, shell=True)


    def registroServicoMovimento(self):
        print("Registrando a classe Movimento no Servidor de nomes")
        with Pyro4.Daemon(Controle.get_ip(self)) as daemon:
            ns = Pyro4.locateNS(Controle.get_ip(self))
            uri = daemon.register(Movimento)
            ns.register("Movimento", uri)
            print("Classe Movimento registarda")
            print(uri)
            daemon.requestLoop()

    def registroServicoServidor(self):
        print("Registrando a classe Servidor no servidor de nomes")
        with Pyro4.Daemon(Controle.get_ip(self)) as daemon:
            ns = Pyro4.locateNS(Controle.get_ip(self))
            uri = daemon.register(ServidorSR)
            ns.register('ServidorSR', uri)
            print("Classe Servidor registarda")
            print(uri)
            daemon.requestLoop()

    def run(self):
        print("Starting ", self.threadID)
        print("ID", self.threadID)
        if self.threadID == 1:
            Controle.startServer(self)
        elif self.threadID == 2:
            Controle.registroServicoMovimento(self)
        else:
            Controle.registroServicoServidor(self)
        print("Exiting ", self.threadID)

#if __name__ == '__main__':
thread1 = Controle(1)
thread2 = Controle(2)
thread3 = Controle(3)
#thread1.start()
#time.sleep(30)
thread2.start()
time.sleep(2)
thread3.start()

########################################################################################################################