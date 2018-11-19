#!/usr/bin/env python3
# coding: utf-8
import socket
import threading
from threading import Thread
from time import sleep, time

import Pyro4
from ev3dev.ev3 import *

from Posicionamento import *
from Autonomo import *
from ServidorSR import *

modoDeJogo = 0

pos = Posicionamento(0, 0, 1)

@Pyro4.expose
@Pyro4.oneway
class Movimento:
    def __init__(self):
        self.power = 35
        self.target = 55
        self.kp = float(0.65)
        self.kd = 1
        self.ki = float(0.02)
        self.direction = -1
        self.minRef = 30
        self.maxRef = 55

        # Conecta os dois LargeMotor às portas B e C.
        self.motorEsquerda = LargeMotor(OUTPUT_C)
        self.motorDireita = LargeMotor(OUTPUT_B)

        # Declara sensores ColorSensor e UltrasonicSensor.
        self.sensorCor = ColorSensor()
        self.sensorUS = UltrasonicSensor()

        # Declara botão de interrupção.
        self.btn = Button()

        # Altera modo do sensor ultrassônico.
        self.sensorUS.mode = 'US-DIST-CM'

        self.comunica = ServidorSR()
        self.aut = Autonomo()
        #self.pos = Posicionamento(0, 0, 1)

    def modoJogo(self, mdj):
        print("modo de jogo: ", mdj)
        global modoDeJogo
        global pos
        self.posAtual = pos
        modoDeJogo = mdj
        # SELECIONA MODO DE JOGO
        if modoDeJogo == 1:  # Autonomo
            print("Consulta estrategia")
            direcao = self.aut.executaEstrategia(self.posAtual)
            self.move(direcao)
        #elif modoDeJogo == 2:  # Manual
        # direcao = self.comunica.setDirecaoManual()
        # self.move(direcao)

    def move(self, direcao):
        # PAUSA DO 5 É PRO MODO AUTÔNOMO
        global pos
        if direcao == 5:
            return

        self.sensorCor.mode = 'COL-COLOR'  # Altera para modo refletido
        cor = self.sensorCor.value()

        if direcao == 0:
            self.frente(cor)
            pass

        elif direcao == 1:
            self.esquerda(cor)
            # Orientacao
            if pos.getOrientacao() == 1:
                pos.setOrientacao(4)
            else:
                pos.setOrientacao(pos.getOrientacao() - 1)
            pass

        elif direcao == 2:
            self.direita(cor)
            # Orientacao
            if pos.getOrientacao() == 4:
                pos.setOrientacao(1)
            else:
                pos.setOrientacao(pos.getOrientacao() + 1)
            pass

        elif direcao == 3:
            self.re(cor)
            self.atualizaOrientacaoRe()
            pass

        print("Valor atual de Y: ", pos.getEixoY())
        print("Valor prox de Y: ", (pos.getEixoY() + 1))

        self.atualizaCoordenada()
        print(pos.paraString())
        self.seguirLinha(self.power, self.target, self.kp, self.kd, self.ki, self.direction, self.minRef, self.maxRef)

        print("Valor atual de Y: ", pos.getEixoY())
        print("Valor prox de Y: ", (pos.getEixoY() + 1))

    def atualizaOrientacaoRe(self):
        if pos.getOrientacao() == 3:
            pos.setOrientacao(1)
        elif pos.getOrientacao() == 4:
            pos.setOrientacao(2)
        else:
            pos.setOrientacao(pos.getOrientacao() + 2)

    def atualizaCoordenada(self):
        if pos.getOrientacao() == 1:  # Norte
            pos.setEixoY(pos.getEixoY() + 1)
        elif pos.getOrientacao() == 2:  # Leste
            pos.setEixoX(pos.getEixoX() + 1)
        elif pos.getOrientacao() == 3:  # Sul
            pos.setEixoY(pos.getEixoY() - 1)
        elif pos.getOrientacao() == 4:  # Oeste
            pos.setEixoX(pos.getEixoX() - 1)

    def frente(self, cor):
        # print("Indo para a frente")
        while (cor != 1) and (cor != 6):  # Enquanto for verde
            cor = self.sensorCor.value()
            self.motorEsquerda.run_forever(speed_sp=100)
            self.motorDireita.run_forever(speed_sp=50)

    def esquerda(self, cor):
        # print("Virando para a esquerda")
        while (cor != 1):
            cor = self.sensorCor.value()
            self.motorEsquerda.stop(stop_action='brake')
            self.motorDireita.run_forever(speed_sp=200)

    def direita(self, cor):
        # print("Virando para a direita")
        # self.frente(cor)
        self.motorDireita.stop(stop_action='brake')
        self.motorEsquerda.run_forever(speed_sp=180)
        sleep(2)
        while (cor != 1):
            cor = self.sensorCor.value()
            self.motorDireita.stop(stop_action='brake')
            self.motorEsquerda.run_forever(speed_sp=200)

    def re(self, cor):
        # print("Marcha a re")
        self.direita(cor)
        self.direita(cor)

    # Função incompleta - VOLTAR PARA A POSIÇÃO ANTERIOR
    def detectarObstaculos(self):
        distancia = self.sensorUS.value() / 10
        if distancia < 10:  # Se há obstáculos
            print("Obstaculo")
            self.sensorCor.mode = 'COL-COLOR'  # Altera para modo cor
            cor = self.sensorCor.value()
            self.direita(cor)
            self.motorEsquerda.run_direct()
            self.motorDireita.run_direct()

    def encontraInterseccao(self):
        self.sensorCor.mode = 'COL-COLOR'  # Altera para modo cor
        cor = self.sensorCor.value()
        if (cor == 3):  # verde
            # self.motorEsquerda.run_forever(speed_sp=10)
            # self.motorDireita.run_forever(speed_sp= 10)
            # sleep(0.5)
            self.motorEsquerda.stop(stop_action='brake')
            self.motorDireita.stop(stop_action='brake')
            return True
        else:
            return False

    def manterNaLinha(self, course, power):
        power_left = power_right = power
        s = (50 - abs(float(course))) / 50
        if course >= 0:
            power_right *= s
            if course > 100:
                power_right = - power
        else:
            power_left *= s
            if course < -100:
                power_left = - power
        return (int(power_left), int(power_right))

    def seguirLinha(self, power, target, kp, kd, ki, direction, minRef, maxRef):

        lastError = error = integral = 0

        self.motorEsquerda.run_direct()
        self.motorDireita.run_direct()

        while not self.btn.any():
            # self.detectarObstaculos()  # Para quando encontra um obstáculo
            self.sensorCor.mode = 'COL-REFLECT'  # Altera para modo refletido
            refRead = self.sensorCor.value()
            error = target - (100 * (refRead - minRef) / (maxRef - minRef))
            derivative = error - lastError
            lastError = error
            integral = float(0.5) * integral + error
            course = (kp * error + kd * derivative + ki * integral) * direction
            for (motor, pow) in zip((self.motorEsquerda, self.motorDireita), self.manterNaLinha(course, power)):
                motor.duty_cycle_sp = pow
            sleep(0.01)  # Aprox. 100Hz

            self.interseccaoEncontrada = self.encontraInterseccao()
            if self.interseccaoEncontrada:
                global modoDeJogo
                self.modoJogo(modoDeJogo)
                break