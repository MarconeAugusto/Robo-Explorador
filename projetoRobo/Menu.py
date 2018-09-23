#!/usr/bin/env python3
# coding: utf-8

# ----------------------------------------
# PROGRAMA DE TESTES
# ----------------------------------------

#from Movimento import *
from Posicionamento import *
from Autonomo import *

#mov = Movimento(40, 55, float(0.65), 1, float(0.02), -1, 41, 63)
#mov.seguirLinha(40, 55, float(0.65), 1, float(0.02), -1, 41, 63)

pos1 = Tesouro(3, 5, 0)
pos2 = Tesouro(10, 5, 0)
pos3 = Tesouro(2, 10, 0)

posRobo = Posicionamento(0,0,1)

lista = [pos1, pos2, pos3]

aut = Autonomo(posRobo, lista)

aut.executaEstrategia()

# aut.ordenaLista()
#
# i = 0
# for n in aut.getListaDeEstrategia():
#     print("Distancia: ", aut.getListaDeEstrategia()[i].getDistanciaAteORobo())
#     print("(", aut.getListaDeEstrategia()[i].getEixoX(), ", ", aut.getListaDeEstrategia()[i].getEixoY(),")\n")
#     i = i+1
