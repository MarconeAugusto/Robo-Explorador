#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *

class InterfaceGrafica:

    def __init__(self, raiz):
        self.fontePadrao = ("Arial", "40")
        self.texto = StringVar()
        self.raiz = raiz

        self.container1 = Frame(raiz)
        self.container2 = Frame(raiz)
        self.container3 = Frame(raiz)
        self.container4 = Frame(raiz)
        self.container5 = Frame(raiz)
        # self.container6 = Frame(raiz)
        # self.container7 = Frame(raiz)
        # self.container8 = Frame(raiz)
        self.container9 = Frame(raiz)
        self.container10 = Frame(raiz)
        self.container11 = Frame(raiz)

        #adicionando os containers
        self.container1.pack()
        self.container2.pack()
        self.container3.pack()
        self.container4.pack()
        self.container5.pack()
        # self.container6.pack()
        # self.container7.pack()
        # self.container8.pack()
        self.container9.pack()
        self.container10.pack()
        self.container11.pack()

        #adicionando os botões aos containers
        self.espaco = Label(self.container1, text='      ', font=self.fontePadrao, pady="100").pack()
        self.b1 = Button(self.container2, text='⬆️',font=self.fontePadrao, command=self.frentePressionado, bg="gray", width=5).pack()
        self.b2 = Button(self.container3, text='⬅️',font=self.fontePadrao, command=self.esquerdaPressionado, bg="gray", width=5).pack(side=LEFT)
        self.b3 = Button(self.container3, text='➡️',font=self.fontePadrao, command=self.direitaPressionado, bg="gray", width=5).pack(side=LEFT)
        self.b4 = Button(self.container4, text= '⬇️', font=self.fontePadrao, command=self.rePressionado, bg="gray", width=5).pack()
        self.espaco = Label(self.container5, text='      ', font=self.fontePadrao, pady="50").pack()
        #self.b5 = Button(self.container6, text='Valida Caça',font=self.fontePadrao, command=self.validaPressionado, bg="gray", width=20).pack()
        #self.b6 = Button(self.container7, text='     Pausa    ', font=self.fontePadrao, command=self.pausaPressionado, bg="gray", width=20).pack()
        #self.b7 = Button(self.container8, text=' Fim de jogo', font=self.fontePadrao, command=self.fimPressionado, bg="gray", width=20).pack()
        self.espaco = Label(self.container9, text='      ', font=self.fontePadrao, pady="50").pack()
        self.dados = Label(self.container10, font=self.fontePadrao, textvariable=self.texto, width="50").pack()
        self.espaco = Label(self.container11, text='      ', font=self.fontePadrao, pady="50").pack()


    def frentePressionado(self):
        #adiconar aqui a implementação do objeto distrído que vai chamar a função move()
        self.texto.set("Movendo para frente...")
        print("Movendo para frente")
        self.direcao = 0
        self.raiz.destroy()


    def esquerdaPressionado(self):
        #adiconar aqui a implementação do objeto distrído que vai chamar a função move()
        self.texto.set("Movendo para esquerda...")
        print("Movendo para esquerda")
        self.direcao = 1
        self.raiz.destroy()


    def direitaPressionado(self):
        #adiconar aqui a implementação do objeto distrído que vai chamar a função move()
        self.texto.set("Movendo para direita...")
        print("Movendo para direita")
        self.direcao = 2
        self.raiz.destroy()


    def rePressionado(self):
        #adiconar aqui a implementação do objeto distrído que vai chamar a função move()
        self.texto.set("Movendo para trás...")
        print("Movendo para trás")
        self.direcao = 3
        self.raiz.destroy()


    def validaPressionado(self):
        #adiconar aqui a implementação do objeto distrído que vai chamar a função validaCaca()
        self.texto.set("Validando caça...")
        print("Validando caça")


    def pausaPressionado(self):
        #adiconar aqui a implementação do objeto distrído que vai chamar a função pausa()
        self.texto.set("Jogo pausado")
        print("Jogo pausado")


    def fimPressionado(self):
        #adiconar aqui a implementação do objeto distrído que vai chamar a função fimDeJogo()
        self.texto.set("Finalizando a partida...")
        print("Finalizando a partida...")
        self.raiz.destroy()


    def desenhar(self):
        self.raiz.title("Modo Manual")
        InterfaceGrafica(self.raiz)
        self.raiz.mainloop()
        return self.direcao