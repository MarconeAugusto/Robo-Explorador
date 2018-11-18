#!/usr/bin/env python3
# coding: utf-8

class Posicionamento:

    def __init__(self, eixoX, eixoY, orientacao):
        self.eixoX = eixoX
        self.eixoY = eixoY
        self.orientacao = orientacao

    def getEixoX(self):
        return self.eixoX

    def getEixoY(self):
        return self.eixoY

    def getOrientacao(self):
        return self.orientacao

    def setEixoX(self, eixoX):
        self.eixoX = eixoX

    def setEixoY(self, eixoY):
        self.eixoY = eixoY

    def setOrientacao(self, orientacao):
        self.orientacao = orientacao

    def paraString(self):
        if self.orientacao == 1:
            return "({}, {}) - NORTE".format(self.eixoX, self.eixoY)
        elif self.orientacao == 2:
            return "({}, {}) - LESTE".format(self.eixoX, self.eixoY)
        elif self.orientacao == 3:
            return "({}, {}) - SUL".format(self.eixoX, self.eixoY)
        else:
            return "({}, {}) - OESTE".format(self.eixoX, self.eixoY)

        #Encontrado no site: https://pyformat.info/