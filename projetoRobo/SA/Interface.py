#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import *

class InterfaceGrafica:

    def __init__(self, dados, mapa):
        self.fontePadrao = ("Arial", "40")
        self.fonteMenor = ("Arial", "30")
        self.textoParadaRobo1 = StringVar()
        self.textoParadaRobo2 = StringVar()
        self.dadosRobo1 = StringVar()
        self.dadosRobo2 = StringVar()
        self.dadosGerais = StringVar()
        self.coordMapaNula = StringVar()
        self.coordMapa = StringVar()
        self.coordCaca = StringVar()
        self.coordRobo1 = StringVar()
        self.coordRobo2 = StringVar()
        self.dados = dados
        self.mapa = mapa

        # --- Cor dos LEDs dos robôs ----
        self.backgroudRobo1 = "red"
        self.backgroudRobo2 = "yellow"

        self.container1 = Frame(mapa)
        self.container2 = Frame(dados)
        self.container3 = Frame(dados)
        self.container4 = Frame(dados)
        self.container5 = Frame(dados)
        self.container6 = Frame(dados)
        self.container7 = Frame(mapa)
        self.container8 = Frame(mapa)
        self.container9 = Frame(mapa)
        self.container10 = Frame(dados)
        self.container11 = Frame(dados)

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

        # ==== Mapa =====
        mapa.geometry("1000x600")
        # mapa.configure(background="Gray")

        self.espaco = Label(self.container1, text='Mapa', font=self.fontePadrao, pady="50").pack()

        linhas = 10
        colunas = 10
        for i in range(0, linhas):
            for j in range(0, colunas):
                # self.cacas = False
                # self.matriz[i][j] = self.cacas

                # ----- ROBÔ -----
                if(i == 0 and j == 0):
                    self.b1 = Button(self.container7, padx='20', pady='10', text="r1")
                    self.b1.grid(row=i, column=j, sticky='news')
                elif (i == 9 and j == 9):
                    self.b1 = Button(self.container7, padx='20', pady='10', text="r2")
                    self.b1.grid(row=i, column=j, sticky='news')

                # ----- CAÇAS ------
                elif (i == 3 and j == 4):
                    self.b1 = Button(self.container7, padx='20', pady='10', text="c")
                    self.b1.grid(row=i, column=j, sticky='news')
                elif (i == 6 and j == 3):
                    self.b1 = Button(self.container7, padx='20', pady='10', text="c")
                    self.b1.grid(row=i, column=j, sticky='news')
                elif (i == 8 and j == 6):
                    self.b1 = Button(self.container7, padx='20', pady='10', text="c")
                    self.b1.grid(row=i, column=j, sticky='news')
                elif (i == 2 and j == 1):
                    self.b1 = Button(self.container7, padx='20', pady='10', text="c")
                    self.b1.grid(row=i, column=j, sticky='news')
                elif (i == 1 and j == 9):
                    self.b1 = Button(self.container7, padx='20', pady='10', text="c")
                    self.b1.grid(row=i, column=j, sticky='news')

                # ----- NÃO HÁ NADA -------
                else:
                    self.b1 = Button(self.container7, padx='20', pady='10', text="  ")
                    self.b1.grid(row=i, column=j, sticky='news')

        # ==== dados iniciais de cada robô ====
        self.cacas1 = 0
        self.cacas2 = 0
        self.pos1 = "(0, 0)"
        self.pos2 = "(20, 20)"
        self.prox1 = "(-, -)"
        self.prox2 = "(-, -)"

        self.dadosRobo1.set('Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.cacas1, self.pos1, self.prox1))
        self.dadosRobo2.set('Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s' % (self.cacas2, self.pos2, self.prox2))

        # ==== dados iniciais gerais ====
        self.totalCacas = 0 # Vê o tamanho da lista de caças
        self.cacasEncontradas = 0
        self.cacasRestantes = (self.totalCacas - self.cacasEncontradas)

        self.dadosGerais.set('Total de caças: %d\n Caças encontradas: %d\n Caças restantes: %d\n' % (self.totalCacas, self.cacasEncontradas, self.cacasRestantes))

        # self.espaco = Label(self.container2, text='Informações', font=self.fontePadrao, pady="50").pack()
        # TRANSFORMAR EM TEXTVARIABLE PARA PODER RECEBER OS NOMES DOS ROBÔS:
        self.textbox = Label(self.container2, text='G1', font=self.fontePadrao, bg = self.backgroudRobo1, width = 20).pack(side=LEFT)
        self.textbox = Label(self.container3, textvariable=self.dadosRobo1, font=self.fonteMenor, bg="gray", width=27, height=5).pack(side=LEFT)
        self.parada = Label(self.container4, font=self.fontePadrao, textvariable=self.textoParadaRobo1, foreground= "red", width=20).pack(side=LEFT)
        self.espaco = Label(self.container2, text='', font=self.fontePadrao, width=5).pack(side=LEFT)
        self.espaco = Label(self.container3, text='', font=self.fontePadrao, width=5).pack(side=LEFT)
        self.espaco = Label(self.container4, text='', font=self.fontePadrao, width=5).pack(side=LEFT)
        self.textbox = Label(self.container2, text='G2', font=self.fontePadrao, bg=self.backgroudRobo2, width = 20).pack(side=RIGHT)
        self.textbox = Label(self.container3, textvariable=self.dadosRobo2, font=self.fonteMenor, bg="gray", width=27, height=5).pack(side=RIGHT)
        self.parada = Label(self.container4, font=self.fontePadrao, textvariable=self.textoParadaRobo2, foreground="red", width=20).pack(side=RIGHT)
        self.textbox = Label(self.container5, textvariable=self.dadosGerais, font=self.fonteMenor, bg="gray", width=61).pack()

        self.b2 = Button(self.container6, text='Obstáculo️', font=self.fontePadrao, command=self.paradaEmergencia, bg="gray", width=20).pack(side=LEFT)
        self.b2 = Button(self.container6, text='Sem obstáculo️', font=self.fontePadrao, command=self.apagaTexto, bg="gray", width=20).pack(side=RIGHT)

    # def verificaListaCacas(self):
    #     self.cacas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def addCaca(self):
        if self.b1["textvariable"] == " ":
            self.b1["textvariable"] = "r1"

    def paradaEmergencia(self):
        self.textoParadaRobo1.set("Parada de emergência")
        print("Obstáculo")
        # ==== dados vindos do SS ====
        self.cacas1 = 2
        self.cacas2 = 1
        self.pos1 = "(10, 5)"
        self.pos2 = "(5, 6)"
        self.prox1 = "(10, 4)"
        self.prox2 = "(6, 6)"
        self.dadosRobo1.set('Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s\n' % (self.cacas1, self.pos1, self.prox1))
        self.dadosRobo2.set('Caças coletadas: %d\n Posição atual: %s \n Próxima posição: %s\n' % (self.cacas2, self.pos2, self.prox2))

        self.totalCacas = 5
        self.cacasEncontradas = 3
        self.cacasRestantes = (self.totalCacas - self.cacasEncontradas)
        self.dadosGerais.set('Total de caças: %d\n Caças encontradas: %d\n Caças restantes: %d' % (self.totalCacas, self.cacasEncontradas, self.cacasRestantes))

    def apagaTexto(self):
        self.textoParadaRobo1.set("")

dados = Tk()
mapa = Tk()
dados.title("Informações")
mapa.title("Mapa")
InterfaceGrafica(dados, mapa)
dados.mainloop()
mapa.mainloop()