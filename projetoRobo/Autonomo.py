#!/usr/bin/env python3
# coding: utf-8

from Movimento import *

class Tesouro:
    def __init__(self, eixoX, eixoY, distanciaAteORobo):
        self.eixoX = eixoX
        self.eixoY = eixoY
        self.distanciaAteORobo = distanciaAteORobo

    def getEixoX(self):
        return self.eixoX

    def getEixoY(self):
        return self.eixoY

    def setEixoX(self, eixoX):
        self.eixoX = eixoX

    def setEixoY(self, eixoY):
        self.eixoY = eixoY

    def getDistanciaAteORobo(self):
        return self.distanciaAteORobo

    def setDistanciaAteORobo(self, distanciaAteORobo):
        self.distanciaAteORobo = distanciaAteORobo

class Autonomo:

    def __init__(self, posAtual, listaDeCacas):

        self.listaDeCacas = listaDeCacas
        self.listaDeEstrategia = []
        self.posAtual = posAtual
        self.pausa = False
        self.finaliza = False
        self.anda = Movimento(40, 55, float(0.65), 1, float(0.02), -1, 41, 63)

        if posAtual.eixoX == 0:
            self.posAdversario = Posicionamento(20,20,3)
        else:
            self.posAdversario = Posicionamento(0, 0, 1)

    def setPosicaoAdvsersario(self, posAdversario):
        self.posicaoAdversario = posAdversario

    def setPosAtual(self, posAtual):
        self.posAtual = posAtual

    def setPosProx(self, posProx):
        self.posProx = posProx

    def getPosicaoAdvsersario(self):
        return self.posicaoAdversario

    def getPosAtual(self):
        return self.posAtual

    def getPosProx(self):
        return self.posProx

    def adicionarTesouro(self, x, y, distancia):
        tesouro = Tesouro(x, y, distancia)
        self.listaDeEstrategia.append(tesouro)

    def ordenaLista(self):

        while len(self.listaDeCacas) != 0:
            self.distanciaMinima = 20
            self.menorI = 0
            self.i = 0

            for n in self.listaDeCacas:
                self.distancia = abs(self.posAtual.getEixoX() + self.posAtual.getEixoX() - (self.listaDeCacas[self.i].getEixoX() + self.listaDeCacas[self.i].getEixoY()));
                if self.distancia < self.distanciaMinima:
                    self.distanciaMinima = self.distancia
                    self.menorI = self.i
                self.i = (self.i+1)

            self.adicionarTesouro(self.listaDeCacas[self.menorI].getEixoX(), self.listaDeCacas[self.menorI].getEixoY(), self.distanciaMinima)
            self.listaDeCacas.pop(self.menorI)

    def getListaDeEstrategia(self):
        return self.listaDeEstrategia

    #CRIAR FUNÇÃO ESTRATÉGIA

    def pausar(self):
        self.pausa = True

    def continuaJogo(self):
        self.pausa = False

    def finalizarJogo(self):
        self.finaliza = True

    def executaEstrategia(self):
        #while not self.finaliza:
        self.ordenaLista()

        # EIXO Y
        if self.listaDeEstrategia[0].getEixoY() < self.getPosAtual().getEixoY(): # SE A CACA ESTA ABAIXO DO ROBO

            if self.getPosAtual().getOrientacao() != 3: # EH NECESSARIO SUL

                if self.getPosAtual().getOrientacao() == 1: # NORTE
                    self.anda.move(3) #RE

                elif self.getPosAtual().getOrientacao() == 2: # Leste
                    self.anda.move(2)  # DIREITA

                else: # OESTE
                    self.anda.move(1)  # ESQUERDA

            while self.listaDeEstrategia[0].getEixoY() != self.getPosAtual().getEixoY():
                self.anda.move(0) #FRENTE


        elif self.listaDeEstrategia[0].getEixoY() > self.getPosAtual().getEixoY():  # SE A CACA ESTA ACIMA DO ROBO

            if self.getPosAtual().getOrientacao() != 1:  # EH NECESSARIO NORTE

                if self.getPosAtual().getOrientacao() == 2:  # LESTE
                    self.anda.move(1)  # ESQUERDA

                elif self.getPosAtual().getOrientacao() == 3:  # SUL
                    self.anda.move(3)  # RE

                else:  # OESTE
                    self.anda.move(2)  # DIREITA

            while self.listaDeEstrategia[0].getEixoY() != self.getPosAtual().getEixoY():
                self.anda.move(0)  # FRENTE

        # EIXO X
        if self.listaDeEstrategia[0].getEixoX() < self.getPosAtual().getEixoX():  # SE A CACA ESTA A ESQUERDA DO ROBO

            if self.getPosAtual().getOrientacao() != 4:  # EH NECESSARIO OESTE

                if self.getPosAtual().getOrientacao() == 1:  # NORTE
                    self.anda.move(1)  # ESQUERDA

                elif self.getPosAtual().getOrientacao() == 2:  # Leste
                    self.anda.move(3)  # RE

                else:  # SUL
                    self.anda.move(2)  # DIREITA

            while self.listaDeEstrategia[0].getEixoX() != self.getPosAtual().getEixoX():
                self.anda.move(0)  # FRENTE


        elif self.listaDeEstrategia[0].getEixoX() > self.getPosAtual().getEixoX():  # SE A CACA ESTA A DIREITA DO ROBO

            if self.getPosAtual().getOrientacao() != 2:  # EH NECESSARIO LESTE

                if self.getPosAtual().getOrientacao() == 1:  # NORTE
                    self.anda.move(2)  # DIREITA

                elif self.getPosAtual().getOrientacao() == 3:  # SUL
                    self.anda.move(1)  # ESQUERDA

                else:  # OESTE
                    self.anda.move(3)  # RE

            while self.listaDeEstrategia[0].getEixoX() != self.getPosAtual().getEixoX():
                self.anda.move(0)  # FRENTE
