#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import subprocess
from tkinter import *
import threading
import time
import Pyro4
from ClienteSR import *
from SS import PrincipalSS

class Packing:

    def __init__(self, instancia_Tk,mdj):

        #modoDeJogo = 2
        self.modoDeJogo = mdj

        if self.modoDeJogo == 1:
            instancia_Tk.title("Modo Autonomo")
            self.fontePadrao = ("Arial", "20")
            self.texto = StringVar()

            self.container1 = Frame(instancia_Tk)
            self.container1.pack()
            self.espaco = Label(self.container1, text='      ', font=self.fontePadrao, pady="20").pack()

        elif self.modoDeJogo == 2:
            instancia_Tk.title("Modo Manual")
            self.fontePadrao = ("Arial", "20")
            self.texto = StringVar()

            self.container1 = Frame(instancia_Tk)
            self.container2 = Frame(instancia_Tk)
            self.container3 = Frame(instancia_Tk)
            self.container4 = Frame(instancia_Tk)
            self.container5 = Frame(instancia_Tk)
            self.container6 = Frame(instancia_Tk)
            self.container7 = Frame(instancia_Tk)
            self.container8 = Frame(instancia_Tk)
            self.container9 = Frame(instancia_Tk)
            self.container10 = Frame(instancia_Tk)
            self.container11 = Frame(instancia_Tk)

            #adicionando os containers
            self.container1.pack()
            self.container2.pack()
            self.container3.pack()
            self.container4.pack()
            self.container5.pack()
            self.container6.pack()
            self.container7.pack()
            self.container8.pack()
            self.container9.pack()
            self.container10.pack()
            self.container11.pack()

            #adicionando os botões aos containers
            self.espaco = Label(self.container1, text='      ', font=self.fontePadrao, pady="20").pack()
            self.b1 = Button(self.container2, text='Frente',font=self.fontePadrao, command=self.frentePressionado, bg="gray", width=20).pack()
            self.b2 = Button(self.container3, text='Esquerda',font=self.fontePadrao, command=self.esquerdaPressionado, bg="gray", width=20).pack(side=LEFT)
            self.b3 = Button(self.container3, text='  Direita  ',font=self.fontePadrao, command=self.direitaPressionado, bg="gray", width=20).pack(side=LEFT)
            self.b4 = Button(self.container4, text= '   Ré   ', font=self.fontePadrao, command=self.rePressionado, bg="gray", width=20).pack()
            self.espaco = Label(self.container5, text='      ', font=self.fontePadrao, pady="50").pack()
            self.b5 = Button(self.container6, text='Valida Caça',font=self.fontePadrao, command=self.validaPressionado, bg="gray", width=20).pack()
            self.b6 = Button(self.container7, text='     Pausa    ', font=self.fontePadrao, command=self.pausaPressionado, bg="gray", width=20).pack()
            self.b7 = Button(self.container8, text=' Fim de jogo', font=self.fontePadrao, command=self.fimPressionado, bg="gray", width=20).pack()
            self.espaco = Label(self.container9, text='      ', font=self.fontePadrao, pady="50").pack()
            self.dados = Label(self.container10, font=self.fontePadrao, textvariable=self.texto, width="50").pack()
            self.espaco = Label(self.container11, text='      ', font=self.fontePadrao, pady="50").pack()

        instancia_Tk.mainloop()

    def frentePressionado(self):
        direcao = 0
        self.texto.set("Movendo para frente...")
        print("Movendo para frente")
        ClienteSR.MovimentoManual(self,direcao)
        #adiconar aqui a implementação do objeto distrído que vai chamar a função move()

    def esquerdaPressionado(self):
        direcao = 1
        self.texto.set("Movendo para esquerda...")
        print("Movendo para esquerda")
        ClienteSR.MovimentoManual(self, direcao)
        #adiconar aqui a implementação do objeto distrído que vai chamar a função move()


    def direitaPressionado(self):
        direcao = 2
        self.texto.set("Movendo para direita...")
        print("Movendo para direita")
        ClienteSR.MovimentoManual(self, direcao)
        #adiconar aqui a implementação do objeto distrído que vai chamar a função move()


    def rePressionado(self):
        direcao = 3
        self.texto.set("Movendo para trás...")
        print("Movendo para trás")
        ClienteSR.MovimentoManual(self, direcao)
        #adiconar aqui a implementação do objeto distrído que vai chamar a função move()


    def validaPressionado(self):
        #adiconar aqui a implementação do objeto distrído que vai chamar a função validaCaca()
        self.texto.set("Validando caça...")
        print("Validando caça")
        PrincipalSS.validaCaca(self)
        #ClienteSR.setCorLed(self)

    def pausaPressionado(self):
        #adiconar aqui a implementação do objeto distrído que vai chamar a função pausa()

        if PrincipalSS.getEstadoDoJogo(self):
            self.texto.set("Jogo pausado")
            print("Jogo pausado")
            estado = False
            PrincipalSS.setEstadoDoJogo(self,estado)
        else:
            self.texto.set("Continua jogo")
            print("Continua jogo")
            estado = True
            PrincipalSS.setEstadoDoJogo(self,estado)

    def fimPressionado(self):
        #adiconar aqui a implementação do objeto distrído que vai chamar a função fimDeJogo()
        self.texto.set("Finalizando a partida...")
        print("Finalizando a partida...")
        #self.raiz.destroy()


class Configuracao(threading.Thread):

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
        Ip = self.get_ip()
        # Ip = ge
        str = "pyro4-ns --host "
        cmd = str + Ip
        print(cmd)
        subprocess.call(cmd, shell=True)

    def registroServidorSS(self):
        print("Registrando no servidor de nomes SS")
        with Pyro4.Daemon(self.get_ip()) as daemon:
            ns = Pyro4.locateNS(self.get_ip())
            uri = daemon.register(PrincipalSS)
            ns.register("listaCacas", uri)
            print("Classe PrincipalSS registrada")
            print(uri)
            daemon.requestLoop()

    def run(self):
        print("Starting ", self.threadID)
        print("ID", self.threadID)
        if self.threadID == 1:
            raiz = Tk()
            Packing(raiz,2)
        elif self.threadID == 2:
            Configuracao.startServer(self)
        elif self.threadID == 3:
            raiz = Tk()
            Packing(raiz, 1)
        elif self.threadID == 4:
            Configuracao.registroServidorSS(self)
        print("Exiting ", self.threadID)
