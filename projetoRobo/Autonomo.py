#!/usr/bin/env python3
# coding: utf-8
import pickle

import Pyro4
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

posAtual = Posicionamento(0,0,1)

class Autonomo:

    def __init__(self):

        # self.listaDeCacas = listaDeCacas
        self.listaDeCacas = []
        self.listaDeEstrategia = []
        #self.posAtual = Posicionamento(0,0,1)
        self.pausa = False
        self.finaliza = False

        # if posAtual.eixoX == 0:
        #     self.posAdversario = Posicionamento(20,20,3)
        # else:
        #     self.posAdversario = Posicionamento(0, 0, 1)

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
        # solicitar a lista de cacas avaliar a mudanca para o SS

        print("Ordena Lista")

        ns = Pyro4.locateNS("191.36.10.123")  # IP do SS
        uri = ns.lookup('listaCacas')
        print(uri)
        self.o = Pyro4.Proxy(uri)
        lista = self.o.getListaCacas()


        if lista == 1:
            print("Lista vazia")


        # enquanto a lista não tiver fim
        tesouro1 = Tesouro(lista[0][0], lista[0][1], 0)
        tesouro2 = Tesouro(lista[1][0], lista[1][1], 0)
        #tesouro3 = Tesouro(lista[2][0], lista[2][1], 0)

        self.listaDeCacas.append(tesouro1)
        #self.listaDeCacas.append(tesouro2)
        #self.listaDeCacas.append(tesouro3)

        # self.listaDeCacas = o.getListaCacas()
        # print(o.getListaCacas())

        while len(self.listaDeCacas) != 0:
            self.distanciaMinima = 20 # No comeco deve ser a maior distancia
            self.menorI = 0
            self.i = 0

            for n in self.listaDeCacas:

                print("POS ATUAL: ", posAtual.getEixoX(), posAtual.getEixoY())
                print("Caca ATUAL: ", self.listaDeCacas[self.i].getEixoX(), self.listaDeCacas[self.i].getEixoY())

                self.distancia = abs(posAtual.getEixoX() + posAtual.getEixoY() - (
                            self.listaDeCacas[self.i].getEixoX() + self.listaDeCacas[self.i].getEixoY())) # getEixoY antes era getEixoX

                print("Distancia: ", self.distancia)

                if self.distancia < self.distanciaMinima:
                    self.distanciaMinima = self.distancia
                    self.menorI = self.i

                self.i = (self.i + 1)

            self.adicionarTesouro(self.listaDeCacas[self.menorI].getEixoX(), self.listaDeCacas[self.menorI].getEixoY(),
                                  self.distanciaMinima)
            print("Remove CACA no SR")
            self.listaDeCacas.pop(self.menorI)

    def getListaDeEstrategia(self):
        return self.listaDeEstrategia

    # CRIAR FUNÇÃO ESTRATÉGIA

    def pausar(self):
        self.pausa = True

    def continuaJogo(self):
        self.pausa = False

    def finalizarJogo(self):
        self.finaliza = True

    def executaEstrategia(self,pos):
        global posAtual
        posAtual = pos
        print("Executa estrategia")
        # while not self.finaliza:
        # obter a lista de cacas no SS
        self.ordenaLista()

        # print(self.listaDeEstrategia[0].getEixoX())
        # print(self.listaDeEstrategia[0].getEixoY())
        # print(self.listaDeEstrategia[0].getDistanciaAteORobo())

        # EIXO Y
        if (self.listaDeEstrategia[0].getEixoY() == posAtual.getEixoY()) and (
                self.listaDeEstrategia[0].getEixoX() == posAtual.getEixoX()):
            if len(self.listaDeEstrategia) > 1:
                print("RETIREI")

                print("Solicita remocao caca no SS")
                self.o.removeCaca(self.menorI)

                self.listaDeEstrategia.pop(0)
                print(self.listaDeEstrategia[0].getEixoX())
                print(self.listaDeEstrategia[0].getEixoY())
                print(self.listaDeEstrategia[0].getDistanciaAteORobo())
            else:
                print("FIM DE JOGO")
                return 5
            print("CHEGUEI!")
            self.executaEstrategia(posAtual)

        if self.listaDeEstrategia[0].getEixoY() < posAtual.getEixoY():  # SE A CACA ESTA ABAIXO DO ROBO
            print("CACA ESTA ABAIXO DO ROBO")
            if posAtual.getOrientacao() != 3:  # EH NECESSARIO SUL

                if posAtual.getOrientacao() == 1:  # NORTE
                    # self.anda.move(3) #RE
                    return 3


                elif posAtual.getOrientacao() == 2:  # Leste
                    # self.anda.move(2)  # DIREITA
                    return 2

                else:  # OESTE
                    # self.anda.move(1)  # ESQUERDA
                    return 1

            else:
                print("VOU PRA FRENTE POIS ACIMA")
                # self.anda.move(0)  # FRENTE
                return 0

        if self.listaDeEstrategia[0].getEixoY() > posAtual.getEixoY():  # SE A CACA ESTA ACIMA DO ROBO
            print("CACA ESTA ACIMA DO ROBO")

            if posAtual.getOrientacao() != 1:  # EH NECESSARIO NORTE

                if posAtual.getOrientacao() == 2:  # LESTE
                    # self.anda.move(1)  # ESQUERDA
                    return 1

                elif posAtual.getOrientacao() == 3:  # SUL
                    # self.anda.move(3)  # RE
                    return 3

                else:  # OESTE
                    # self.anda.move(2)  # DIREITA
                    return 2

            else:
                print("VOU PRA FRENTE POIS ACIMA")
                # self.anda.move(0)  # FRENTE
                return 0

            # while self.listaDeEstrategia[0].getEixoY() != self.getPosAtual().getEixoY():
            #     self.anda.move(0)  # FRENTE

        # EIXO X
        if self.listaDeEstrategia[0].getEixoX() < posAtual.getEixoX():  # SE A CACA ESTA A ESQUERDA DO ROBO
            print("CACA ESTA A ESQUERDA DO ROBO")

            if posAtual.getOrientacao() != 4:  # EH NECESSARIO OESTE

                if posAtual.getOrientacao() == 1:  # NORTE
                    # self.anda.move(1)  # ESQUERDA
                    return 1

                elif posAtual.getOrientacao() == 2:  # Leste
                    # self.anda.move(3)  # RE
                    return 3

                else:  # SUL
                    # self.anda.move(2)  # DIREITA
                    return 2

            else:
                print("VOU PRA FRENTE POIS ACIMA")
                # self.anda.move(0)  # FRENTE
                return 0


        elif self.listaDeEstrategia[0].getEixoX() > posAtual.getEixoX():  # SE A CACA ESTA A DIREITA DO ROBO
            print("CACA ESTA A DIREITA DO ROBO")

            if posAtual.getOrientacao() != 2:  # EH NECESSARIO LESTE

                if posAtual.getOrientacao() == 1:  # NORTE
                    # self.anda.move(2)  # DIREITA
                    return 2

                elif posAtual.getOrientacao() == 3:  # SUL
                    # self.anda.move(1)  # ESQUERDA
                    return 1

                else:  # OESTE
                    # self.anda.move(3)  # RE
                    return 3

            else:
                # self.anda.move(0)  # FRENTE
                return 0

        # print("VOU EXECUTAR A ESTRATEGIA DE NOVO")
        # self.executaEstrategia()

        # while self.listaDeEstrategia[0].getEixoX() != self.getPosAtual().getEixoX():
        #     self.anda.move(0)  # FRENTE
