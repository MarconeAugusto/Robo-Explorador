from threading import Thread, Event, Lock
from time import sleep
import json
from projetoRobo.SA.gerenciador import *
from projetoRobo.SA.mensagens_auditor import MsgSAtoSS
from copy import deepcopy
import random
import projetoRobo.SA.compartilhados
from projetoRobo.SA import compartilhados

if __name__ == '__main__':
	gerente = Gerenciador()
	gerente.init_thread_rede()

	print("*** Antes de mais nada, cadastre o robo !!! ***")
	print("Este nome sera usado para as mensagens enviadas ao robo")

	nome = ''
	while True:
		print("""
 ### Escolha a opcao de mensagem:
1) Cadastra robo
2) Solicita ID
3) Solicita Historico
4) Solicita Status
5) Novo Jogo
6) Pausa
7) Continua
8) Fim Jogo
9) Atualiza Mapa
0) EXIT
		""")


		op = input("Opcao: ")
		msg = {"_dir": "teste", "_robo": nome}
		try:
			op = int(op)
			if op == 1:
				# Cadastra robo
				nome = input("Nome: ")
				cor = int(input("Cor (int):"))
				mac = input("MAC: ")
				gerente.cadastra_robo(nome, cor, mac)
				msg.update({"cmd": MsgSAtoSS.CadastraRobo, "nome": nome, "cor": cor, "mac": mac, "_robo": nome})

			elif op == 2:
				# Solicita ID
				msg.update({"cmd": MsgSAtoSS.SolicitaID})

			elif op == 3:
				# Solicita historico
				msg.update({"cmd": MsgSAtoSS.SolicitaHistorico})

			elif op == 4:
				# Solicita historico
				msg.update({"cmd": MsgSAtoSS.SolicitaStatus})

			elif op == 5:
				modo = int(input("Digite 1 para manual e 2 para automatico: "))
				x = int(input("Posicao inicial X: "))
				y = int(input("Posicao inicial Y: "))
				cacas = []
				if int(modo) == 2:
					# Sorteia cacas
					for i in range(0, 5):
						caca = {}
						caca["x"] = random.randint(0, 6)
						caca["y"] = random.randint(0, 6)
						cacas.append(caca)

					print("Cacas: %s" % str(cacas))

				msg.update({"cmd": MsgSAtoSS.NovoJogo, "modo_jogo": modo,
							"x": x, "y": y, "cacas": cacas})

			elif op == 6:
				# Pausa
				msg.update({"cmd": MsgSAtoSS.Pausa})

			elif op == 7:
				# Continua
				msg.update({"cmd": MsgSAtoSS.Continua})

			elif op == 8:
				# Fim Jogo
				msg.update({"cmd": MsgSAtoSS.FimJogo})

			elif op == 9:
				print("Apenas uma caca ...")
				x = int(input("Caca (X): "))
				y = int(input("Caca (Y): "))
				adv_x = random.randint(0, 6)
				adv_y = random.randint(0, 6)
				print("Posicao Fake adversario: (%d,%d)" % (adv_x, adv_y))
				cacas = [{"x": x, "y": y}]
				adv = {"x": adv_x, "y": adv_y}
				msg.update({"cmd": MsgSAtoSS.AtualizaMapa, "cacas": cacas, "posicao_adversario": adv})

			elif op == 0:
				msg = {"cmd": -1, "_dir": "local"}

			else:
				continue

		except:
			print("Opcao invalida")
			continue

		print("msg: %s" % str(msg))
		with compartilhados.gerente_msg_lock:
			compartilhados.gerente_msg = deepcopy(msg)
			compartilhados.solicita_gerente.set()

		sleep(2)

		if op == 0: break