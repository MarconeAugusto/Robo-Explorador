#!/usr/bin/env python3
# coding: utf-8

from time import sleep
from ev3dev.ev3 import *

# ------Input--------
power = 40			#Potência do motor.
target = 55
kp = float(0.65) 	# Proportional gain. Start value 1.
kd = 1           	# Derivative gain. Start value 0.
ki = float(0.02) 	# Integral gain. Start value 0.
direction = -1 		# Define a borda da linha que o sensor de cor seguirá.
minRef = 41			# Valor mínimo refletido.
maxRef = 63			# Valor máximo refletido.
# -------------------

# Conecta os dois LargeMotor às portas B e C.
left_motor = LargeMotor(OUTPUT_C)
right_motor = LargeMotor(OUTPUT_B)

# Declara sensores ColorSensor e UltrasonicSensor.
sensorCor = ColorSensor()
sensorUS = UltrasonicSensor()

# Declara botão de interrupção.
btn = Button()

# Altera modo do sensor ultrassônico.
sensorUS.mode='US-DIST-CM'

def vira():
	direcao = input("Informe a direcao: ")
	
	cor = sensorCor.value()
	if direcao == '0':
		frente(cor)
		pass
	
	elif direcao == '1':
		esquerda(cor)
		pass
		
	elif direcao == '2':
		direita(cor)
		pass
	
	elif direcao == '3':
		re(cor)
		pass
	
	seguirLinha(power, target, kp, kd, ki, direction, minRef, maxRef)



def frente(cor):
	print("Indo para a frente")
	while (cor != 1) and (cor != 6): # Enquanto for verde
		cor = sensorCor.value()
		left_motor.run_forever(speed_sp=100)
		right_motor.run_forever(speed_sp=50)



def esquerda(cor):
	print("Virando para a esquerda")
	while (cor != 1) and (cor != 6): # Enquanto for verde
		cor = sensorCor.value()
		left_motor.stop(stop_action='brake')
		right_motor.run_forever(speed_sp=100)
	while (cor != 1):
		cor = sensorCor.value()
		left_motor.stop(stop_action='brake')
		right_motor.run_forever(speed_sp=200)
	
def direita(cor):
	#print("Virando para a direita")
	frente(cor)
		
	right_motor.stop(stop_action='brake')
	left_motor.run_forever(speed_sp=200)
	sleep(1)
	sleep(1)
	
	while (cor != 1):
		cor = sensorCor.value()
		right_motor.stop(stop_action='brake')
		left_motor.run_forever(speed_sp=200)

def re(cor):
	print("Marcha a re")
	direita(cor)
	direita(cor)

# Função incompleta - VOLTAR PARA A POSIÇÃO ANTERIOR
def detectarObstaculos():
	distancia = sensorUS.value()/10
	if distancia < 10: # Se há obstáculos
		print("Obstaculo")
		sensorCor.mode='COL-COLOR'		# Altera para modo cor
		cor = sensorCor.value()
		direita(cor)
		left_motor.run_direct()
		right_motor.run_direct()

'''
def encontraInterseccao():
	sensorCor.mode='COL-COLOR'		# Altera para modo cor
	cor = sensorCor.value()
	if (cor != 1) and (cor != 6):
		left_motor.stop(stop_action='brake')
		right_motor.stop(stop_action='brake')
		return True
	else:
		return False

'''

def encontraInterseccao():
	sensorCor.mode='COL-COLOR'		# Altera para modo cor
	cor = sensorCor.value()
	if (cor == 3):
		left_motor.stop(stop_action='brake')
		right_motor.stop(stop_action='brake')
		return True
	else:
		return False

def manterNaLinha(course, power):
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



def seguirLinha(power, target, kp, kd, ki, direction, minRef, maxRef):

	lastError = error = integral = 0
	
	interseccaoEncontrada = encontraInterseccao()
	if interseccaoEncontrada: # Encontra a intersecção da posição incial
		vira()
		
	left_motor.run_direct()
	right_motor.run_direct()
	
	while not btn.any() :
		
		detectarObstaculos() # Para quando encontra um obstáculo
		
		sensorCor.mode = 'COL-REFLECT'	# Altera para modo refletido
		refRead = sensorCor.value()
		error = target - (100 * ( refRead - minRef ) / ( maxRef - minRef ))
		derivative = error - lastError
		lastError = error
		integral = float(0.5) * integral + error
		course = (kp * error + kd * derivative +ki * integral) * direction
		for (motor, pow) in zip((left_motor, right_motor), manterNaLinha(course, power)):
			motor.duty_cycle_sp = pow
		sleep(0.01) # Aprox. 100Hz
		
		interseccaoEncontrada = encontraInterseccao()
		if interseccaoEncontrada:
			vira()
			break

seguirLinha(power, target, kp, kd, ki, direction, minRef, maxRef)

# Para os motores após sair do looping.
left_motor.stop(stop_action='brake')
right_motor.stop(stop_action='brake')

'''
REFERÊNCIAS

As funções seguirLinha e guiarPelaLinha são adaptações do código orinigal disponível em: 
https://github.com/Klabbedi/ev3
'''
