from threading import Thread, Lock, Event
from projetoRobo.SA.mensagens_auditor import *
from projetoRobo.SA.gerente_db import GerenteDB
from projetoRobo.SA.transmissor import *
from projetoRobo.SA.receptor import *
from copy import deepcopy
import projetoRobo.SA.compartilhados
from projetoRobo.SA import compartilhados

class Gerenciador():
	"""Gerenciador do SA. Trata mensagens vindas de qualquer lugar."""

	def __init__(self):
		compartilhados.init()

		# Inicializa o banco de dados
		self.gerente_db = GerenteDB()
		self.gerente_db.cria_db()

		# Inicializa transmissor
		self.transmissor = Transmissor("localhost")
		self.transmissor.start()

		# Inicializa receptor
		self.receptor = Receptor("localhost")
		self.receptor.start()

		super(Gerenciador, self).__init__()


	def get_cadastros(self):
		return self.gerente_db.get_cadastros()


	def cadastra_robo(self, nome, cor, mac):
		return self.gerente_db.cadastra_robo(nome, cor, mac)


	def salva_historico(self, robo_a, cacas_a, robo_b, cacas_b):
		self.gerente_db.salva_partida(robo_a, cacas_a, robo_b, cacas_b)


	def get_historico(self):
		return self.gerente_db.get_partidas()


	def _envia_msg_ss(self, msg):
		with compartilhados.transmitir_msg_lock:
			compartilhados.transmitir_msg = msg
			compartilhados.transmitir_event.set()

	def init_thread_rede(self):
		def gerencia_msg_rede():

			while True:
				# Espera alguma mensagem ...
				compartilhados.solicita_gerente.wait()

				with compartilhados.gerente_msg_lock:
					msg = deepcopy(compartilhados.gerente_msg)

					if 'cmd' not in msg:
						compartilhados.solicita_gerente.clear()
						continue

					cmd = msg['cmd']

					if '_dir' in msg and msg['_dir'] == 'local' and cmd == -1:
						break

					# Solicitacoes vindas do SS
					if '_dir' in msg and msg['_dir'] == 'ss':
						print("Recebi msg do SS: ")
						print("%s \n" % str(msg))
						if cmd == MsgSStoSA.MovendoPara:
							# Avisa interface usuario
							print("OK, funcionando ...")
							pass

						elif cmd == MsgSStoSA.PosicaoAtual:
							# Avisa interface usuario
							pass

						elif cmd == MsgSStoSA.ValidaCaca:
							# Teste: valida tudo
							print("Recebido valida caca. Validando ...")
							msg = {"cmd": MsgSAtoSS.ValidacaoCaca, "ack": 1, "_robo": msg['robo']}
							self._envia_msg_ss(msg)
							pass

						elif cmd == MsgSStoSA.ObstaculoEncontrado:
							# Avisa interface usuario
							pass

						elif cmd == MsgSStoSA.SolicitaID_Resp:
							# Avisa interface usuario
							pass

						elif cmd == MsgSStoSA.SolicitaHistorico_RESP:
							# Avisa interface usuario
							pass

						elif cmd == MsgSStoSA.SolicitaStatus_RESP:
							# Avisa interface usuario
							pass

						else:
							# Comando nao identificado, nao faz nada ...
							pass

					# Solicitacoes vindas da interface de usuario
					elif '_dir' in msg and msg['_dir'] == 'ui':
						'''
						Sugestao: as classes interface usuario e principal
						podem se comunicar com o gerente da mesma forma que
						o SS se comunica com o SA (atraves de mensagens JSON).
						Isto deve facilitar a implementacao, pois ja temos
						o cenario montado, basta criar os IF's ...
	
						if cmd == MsgUItoGerente.NovoJogo:
							# Transmite para SS
	
						elif ...
						'''

					# Solicitacoes vindas da classe principal
					elif '_dir' in msg and msg['_dir'] == 'pr':
						# Aqui podemos fazer da mesma forma ...
						pass

					elif '_dir' in msg and msg['_dir'] == 'teste':
						# No teste, so envia para baixo ...
						with compartilhados.transmitir_msg_lock:
							compartilhados.transmitir_msg = msg
							compartilhados.transmitir_event.set()

					compartilhados.solicita_gerente.clear()

		t = Thread(target=gerencia_msg_rede)
		t.start()
		return


'''
### TESTE:
if __name__ == '__main__':
	print("Inicializando ...")
	gerente = Gerenciador()
	gerente.init_thread_rede()

	for i in range(1, 3):
		print("\nCadastrando %dº robo" % i)
		try:
			nome = input("Nome: ")
			cor = int(input("Cor (int): "))
			mac = input("MAC: ")
		except:
			print("Invalido")
			exit()

		gerente.cadastra_robo(nome, cor, mac)

	print("\nSalvando historico")
	try:
		roboA = input("Primeiro robo: ")
		roboB = input("Segundo robo: ")
		cacasA = int(input("Cacas encontradas primeiro robo (int): "))
		cacasB = int(input("Cacas encontradas segundo robo (int): "))
	except:
		print("Invalido")
		exit()

	gerente.salva_historico(roboA, cacasA, roboB, cacasB)

	print("\nExibindo cadastros ... ")
	cadastros = gerente.get_cadastros()
	for cadastro in cadastros:
		print(cadastro)

	print("\nExibindo historico ... ")
	partidas = gerente.get_historico()
	for partida in partidas:
		print(partida)

	import time
	time.sleep(2)
	print("\nMandando msg por thread ... ")

	with gerente_msg_lock:
		gerente_msg = {'cmd': MsgSStoSA.MovendoPara, '_dir': 'ss'}
		solicita_gerente.set()

	time.sleep(2)
	print("\nEnviando msg para finalizar!!")
	with gerente_msg_lock:
		gerente_msg = {'cmd': -1, '_dir': 'local'}
		solicita_gerente.set()

	print("FIM")
'''
