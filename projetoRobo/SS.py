#!/usr/bin/env python3
# coding: utf-8
import socket
import time
import subprocess
from threading import Thread

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

def iniciarServidorPyro():
    print("Iniciando servidor Pyro:")
    cmd = "pyro4-ns --host "+ get_ip()
    subprocess.call([cmd], shell=True)

def iniciarServidorSS():
    print("\n\nIniciando servidor SS:")
    #SR_SS = SupervisorioSR_SS()

t1 = Thread(target=iniciarServidorPyro)
t2 = Thread(target=iniciarServidorSS)

t1.start()
time.sleep(5)
from SupervisorioSR_SS import *  #####################################
t2.start()