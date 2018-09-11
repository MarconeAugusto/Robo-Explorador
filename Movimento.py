#!/usr/bin/env python3
# coding: utf-8

from time import sleep
from ev3dev.ev3 import *

# ------Input--------
power = 30		#Potência do motor.
target = 55
kp = float(0.65) 	# Proportional gain. Start value 1.
kd = 1           	# Derivative gain. Start value 0.
ki = float(0.02) 	# Integral gain. Start value 0.
direction = -1 		# Define a borda da linha que o sensor de cor seguirá.
minRef = 41		# Valor mínimo refletido.
maxRef = 63		# Valor máximo refletido.
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
	print(direcao)
	
	cor = sensorCor.value()
	if direcao == '1':
		print("Virando para a esquerda")
		while (cor != 1) and (cor != 6): # Enquanto for verde
			left_motor.stop(stop_action='brake')
			right_motor.run_forever(speed_sp=100)
			cor = sensorCor.value()
		pass
		
	elif direcao == '2':
		print("Virando para a direita")
		
		while (cor != 1) and (cor != 6): # Enquanto for verde 
			right_motor.run_forever(speed_sp=-50)
			left_motor.run_forever(speed_sp=100) # encontra preto, branco e outro preto (Verificar)
			cor = sensorCor.value()
		right_motor.run_forever(speed_sp=0)
		left_motor.run_forever(speed_sp=100)
		sleep(0.8)
		pass
	seguirLinha(power, target, kp, kd, ki, direction, minRef, maxRef)

def paradaDeEmergencia():
	distancia = sensorUS.value()/10 
	while distancia < 10: # Enquanto a distância for menor que 10 cm
		right_motor.stop(stop_action='brake')
		left_motor.stop(stop_action='brake')
		distancia = sensorUS.value()/10

def guiarPelaLinha(course, power):
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
	left_motor.run_direct()
	right_motor.run_direct()
	while not btn.any() :
	
		paradaDeEmergencia() # Para quando encontra um obstáculo
		
		sensorCor.mode = 'COL-REFLECT'	# Altera para modo refletido
		refRead = sensorCor.value()
		error = target - (100 * ( refRead - minRef ) / ( maxRef - minRef ))
		derivative = error - lastError
		lastError = error
		integral = float(0.5) * integral + error
		course = (kp * error + kd * derivative +ki * integral) * direction
		for (motor, pow) in zip((left_motor, right_motor), guiarPelaLinha(course, power)):
			motor.duty_cycle_sp = pow
		sleep(0.01) # Aprox. 100Hz
		
		sensorCor.mode='COL-COLOR'	# Altera para modo cor
		cor = sensorCor.value()
		if (cor != 1) and (cor != 6):
			left_motor.stop(stop_action='brake')
			right_motor.stop(stop_action='brake')
			vira()
			break
			
while not btn.any() :
	seguirLinha(power, target, kp, kd, ki, direction, minRef, maxRef)

# Para os motores após sair do looping.
left_motor.stop(stop_action='brake')
right_motor.stop(stop_action='brake')

'''
REFERÊNCIAS

As funções seguirLinha e guiarPelaLinha são adaptações do código orinigal disponível em: 
https://github.com/Klabbedi/ev3
'''
