#!/usr/bin/env python3
# coding: utf-8
from threading import Thread

from self import self
from InterfaceGrafica import *
from Posicionamento import *

teste = True

a = 1 #Autonomo
#a = 2 #Manual

posAtual = Posicionamento(0, 0, 1)
posProx = Posicionamento(0, 0, 1)

pos1 = [2,2]
pos2 = [1,1]
pos3 = [3,3]

estado = True

#lista2 = [pos1, pos2, pos3]
lista2 = [pos1, pos2]
#lista2 = [pos2]

@Pyro4.expose
@Pyro4.oneway
class PrincipalSS(threading.Thread):
    def configInicial(self):
        print("Obtendo MAC Address...")
        print("MAC: ",ClienteSR.getEndMAC(self))

        corLED = input("Informe a cor do LED: ")
        print("Cor escolhida: ", ClienteSR.setCorLed(self, corLED))


    def modoJogo(self):
        global a

        t = PrincipalSS()
        t.start() # Inicia configInicial
        t.join() # Aguarda que configInicial termine

        if a == 2:  # modo Manual
            # Create new threads
            thread1 = Configuracao(1)
            thread2 = Configuracao(2)
            thread4 = Configuracao(4)

            # Start new Threads
            thread1.start()
            time.sleep(1)
            thread2.start()
            time.sleep(1)
            thread4.start()

        elif a == 1:  # modo autonomo
            print("Implementar modo Autonomo")
            # Create new threads
            thread2 = Configuracao(2)  # inicia servidor Pyro4 do SS
            thread3 = Configuracao(3)  # inicia interface Autonomo , alterar depois
            thread4 = Configuracao(4)  # Registra o servidor de nomes
            # Start new Threads
            thread2.start()
            time.sleep(1)
            thread3.start()
            thread4.start()
            time.sleep(1)
            ClienteSR.MovimentoAutonomo(self)

    def getListaCacas(self):
        global lista2
        #global teste
        #print("Lista enviada: ", lista2)
        # if teste:
        #     print("Removendo posicao aleatoria")
        #     lista2.pop(1)
        #     teste = False

        if len(lista2) != 0:
            return lista2
        else:
            return 1

    def removeCaca(self, x,y):
        global lista2
        if len(lista2) == 0:
            print("LISTA VAZIA NO SS")
        else:
            self.i = 0
            for n in lista2:
                if (lista2[self.i][0] == x and lista2[self.i][1] == y):
                    #print("Posição a ser removida", lista2[self.i])
                    lista2.pop(self.i)
                    #print("LISTA ATUALIZADA NO SS: ", lista2)
                self.i = self.i + 1

    def validaCaca(self):
        opt = input("Minha caça é válida?\n"
                    "1) Válida\n"
                    "2) Não válida\n"
                    "Opção: ")
        if opt == '1':
            print("Caça validada")
            return True
        else:
            print("Essa caça não é sua")
            return True

    def atualizaPosicaoSS(self, x, y, ori, id):
        global posAtual
        global posProx

        if id == 1:
            posAtual.setEixoX(x)
            posAtual.setEixoY(y)
            posAtual.setOrientacao(ori)
            print("PosAtual:  ", posAtual.paraString())
        else:
            posProx.setEixoX(x)
            posProx.setEixoY(y)
            posProx.setOrientacao(ori)
            print("posProx:  ", posProx.paraString())

    def setEstadoDoJogo(self, estd):
        global estado
        estado = estd

    def getEstadoDoJogo(self):
        global estado
        return estado

    def run(self):
        PrincipalSS.configInicial(self)

if __name__ == '__main__':
    PrincipalSS.modoJogo(self)
