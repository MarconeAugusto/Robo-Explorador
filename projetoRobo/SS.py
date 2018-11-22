#!/usr/bin/env python3
# coding: utf-8
from self import self
from InterfaceGrafica import *

a = 1

pos1 = [2,2]
pos2 = [1,1]
pos3 = [3,3]
lista2 = [pos1, pos2, pos3]
#lista2 = [pos1]

@Pyro4.expose
@Pyro4.oneway
class PrincipalSS:
    def modoJogo(self):
        global a
        if a == 2:  # modo Manual
            # Create new threads
            thread1 = Configuracao(1)
            # Start new Threads
            thread1.start()
        if a == 1:  # modo autonomo
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
        print("Lista enviada: ", lista2)

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
                    print("Posição a ser removida", lista2[self.i])
                    lista2.pop(self.i)
                    print("LISTA ATUALIZADA: ", lista2)
                self.i = self.i + 1


if __name__ == '__main__':
    PrincipalSS.modoJogo(self)
