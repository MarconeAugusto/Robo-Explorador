#!/usr/bin/env python3
# coding: utf-8

from time import sleep
from ev3dev.ev3 import *
from Posicionamento import *

class Movimento:

    def __init__(self, power, target, kp, kd, ki, direction, minRef, maxRef):
        self.power = power
        self.target = target
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.direction = direction
        self.minRef = minRef
        self.maxRef = maxRef

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

        self.pos = Posicionamento(0,0,1)

    def move(self, direcao):

        #self.direcao = direcao

        #direcao = input("Informe a direcao: ")

        cor = self.sensorCor.value()
        if direcao == '0':
            self.frente(cor)
            pass

        elif direcao == '1':
            self.esquerda(cor)

            # Orientacao
            if self.pos.getOrientacao() == 1:
                self.pos.setOrientacao(4)


            else:
                self.pos.setOrientacao(self.pos.getOrientacao() - 1)
            pass


        elif direcao == '2':
            self.direita(cor)

            # Orientacao
            if self.pos.getOrientacao() == 4:
                self.pos.setOrientacao(1)
            else:
                self.pos.setOrientacao(self.pos.getOrientacao() + 1)
            pass

        elif direcao == '3':
            self.re(cor)

            if self.pos.getOrientacao() == 3:
                self.pos.setOrientacao(1)

            elif self.pos.getOrientacao() == 4:
                self.pos.setOrientacao(2)

            else:
                self.pos.setOrientacao(self.pos.getOrientacao() + 2)
            pass

        if self.pos.getOrientacao() == 1:  # Norte
            self.pos.setEixoY(self.pos.getEixoY() + 1)

        elif self.pos.getOrientacao() == 2:  # Leste
            self.pos.setEixoX(self.pos.getEixoX() + 1)

        elif self.pos.getOrientacao() == 3:  # Sul
            self.pos.setEixoY(self.pos.getEixoY() - 1)

        elif self.pos.getOrientacao() == 4:  # Oeste
            self.pos.setEixoX(self.pos.getEixoX() - 1)

        print(self.pos.paraString())
        self.seguirLinha(self.power, self.target, self.kp, self.kd, self.ki, self.direction, self.minRef, self.maxRef)

    def frente(self, cor):
        #print("Indo para a frente")
        while (cor != 1) and (cor != 6):  # Enquanto for verde
            cor = self.sensorCor.value()
            self.motorEsquerda.run_forever(speed_sp=100)
            self.motorDireita.run_forever(speed_sp=50)

    def esquerda(self, cor):
        #print("Virando para a esquerda")
        while (cor != 1) and (cor != 6):  # Enquanto for verde
            cor = self.sensorCor.value()
            self.motorEsquerda.stop(stop_action='brake')
            self.motorDireita.run_forever(speed_sp=100)
        while (cor != 1):
            cor = self.sensorCor.value()
            self.motorEsquerda.stop(stop_action='brake')
            self.motorDireita.run_forever(speed_sp=200)

    def direita(self, cor):
        #print("Virando para a direita")
        self.frente(cor)

        self.motorDireita.stop(stop_action='brake')
        self.motorEsquerda.run_forever(speed_sp=200)
        sleep(1)
        sleep(1)

        while (cor != 1):
            cor = self.sensorCor.value()
            self.motorDireita.stop(stop_action='brake')
            self.motorEsquerda.run_forever(speed_sp=200)

    def re(self, cor):
        #print("Marcha a re")
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

        #interseccaoEncontrada = self.encontraInterseccao()
        #if interseccaoEncontrada:  # Encontra a intersecção da posição incial
            #self.move()
        #    return
        self.motorEsquerda.run_direct()
        self.motorDireita.run_direct()

        while not self.btn.any():

            self.detectarObstaculos()  # Para quando encontra um obstáculo

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

            interseccaoEncontrada = self.encontraInterseccao()
            if interseccaoEncontrada:
                #self.move()
                break

    '''
    REFERÊNCIAS
    
    As funções seguirLinha e guiarPelaLinha são adaptações do código orinigal disponível em: 
    https://github.com/Klabbedi/ev3
    '''
