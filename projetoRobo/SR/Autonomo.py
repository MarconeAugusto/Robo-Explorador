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
        self.listaDeCacas = []
        self.listaDeEstrategia = []
        self.menorI = 0

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
        print("Ordena lista")
        ns = Pyro4.locateNS("191.36.15.99")  # IP do SS
        uri = ns.lookup('listaCacas')
        self.o = Pyro4.Proxy(uri)
        lista = self.o.getListaCacas()

        if lista == 1:
            print("Lista vazia")
            return 1

        # enquanto a lista não tiver fim
        while len(lista) != 0:
            self.j = 0
            for n in lista:
                self.listaDeCacas.append(Tesouro(lista[self.j][0], lista[self.j][1], 0))
                lista.pop(self.j)
                self.j = self.j + 1

        while len(self.listaDeCacas) != 0:
            self.distanciaMinima = 20 # NAO ALTERAR PARA VALORES MENORES QUE 13, No comeco deve ser a maior distancia
            self.menorI = 0
            self.i = 0

            for n in self.listaDeCacas:
                self.distancia = abs(posAtual.getEixoX() + posAtual.getEixoY()-(self.listaDeCacas[self.i].getEixoX() + self.listaDeCacas[self.i].getEixoY())) # getEixoY antes era getEixoX

                if self.distancia < self.distanciaMinima:
                    self.distanciaMinima = self.distancia
                    self.menorI = self.i
                self.i = (self.i + 1)

            self.adicionarTesouro(self.listaDeCacas[self.menorI].getEixoX(), self.listaDeCacas[self.menorI].getEixoY(),self.distanciaMinima)
            self.listaDeCacas.pop(self.menorI)

    def getListaDeEstrategia(self):
        return self.listaDeEstrategia

    def executaEstrategia(self,pos):
        print("Executa estrategia")
        global posAtual

        posAtual = pos

        self.ordenaLista()

        print("Lista de estrategia : [" ,self.listaDeEstrategia[0].getEixoX(),",",self.listaDeEstrategia[0].getEixoY(), "]")

        #verifica se o robo esta na posicao da lista
        if (self.listaDeEstrategia[0].getEixoY() == posAtual.getEixoY()) and (self.listaDeEstrategia[0].getEixoX() == posAtual.getEixoX()):

            print("CHEGUEI!")

            self.o.validaCaca()

            print("Solicita remocao caca no SS: X =" ,self.listaDeEstrategia[0].getEixoX(),"Y =", self.listaDeEstrategia[0].getEixoY() )
            self.o.removeCaca(self.listaDeEstrategia[0].getEixoX(),self.listaDeEstrategia[0].getEixoY())
            self.listaDeEstrategia.pop(0)

            erro = self.ordenaLista()
            if erro == 1: # AO INVES DE ORDENAR A LISTA NOVAMENTE, TENTAR OBTER SO O TAMANHO DELA
                print("lista de estrategia vazia")
                return 5

        if self.listaDeEstrategia[0].getEixoY() < posAtual.getEixoY():  # SE A CACA ESTA ABAIXO DO ROBO
            if posAtual.getOrientacao() != 3:  # EH NECESSARIO SUL
                if posAtual.getOrientacao() == 1:  # NORTE
                    return 3
                elif posAtual.getOrientacao() == 2:  # Leste
                    return 2
                else:  # OESTE
                    return 1
            else:
                return 0

        if self.listaDeEstrategia[0].getEixoY() > posAtual.getEixoY():  # SE A CACA ESTA ACIMA DO ROBO
            if posAtual.getOrientacao() != 1:  # EH NECESSARIO NORTE
                if posAtual.getOrientacao() == 2:  # LESTE
                    return 1
                elif posAtual.getOrientacao() == 3:  # SUL
                    return 3
                else:  # OESTE
                    return 2
            else:
                return 0

        if self.listaDeEstrategia[0].getEixoX() < posAtual.getEixoX():  # SE A CACA ESTA A ESQUERDA DO ROBO
            if posAtual.getOrientacao() != 4:  # EH NECESSARIO OESTE
                if posAtual.getOrientacao() == 1:  # NORTE
                    return 1
                elif posAtual.getOrientacao() == 2:  # Leste
                    return 3
                else:  # SUL
                    return 2
            else:
                return 0

        elif self.listaDeEstrategia[0].getEixoX() > posAtual.getEixoX():  # SE A CACA ESTA A DIREITA DO ROBO
            if posAtual.getOrientacao() != 2:  # EH NECESSARIO LESTE
                if posAtual.getOrientacao() == 1:  # NORTE
                    return 2
                elif posAtual.getOrientacao() == 3:  # SUL
                    return 1
                else:  # OESTE
                    return 3
            else:
                return 0
