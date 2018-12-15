import sqlite3
from datetime import datetime

class GerenteDB(object):
	"""Responsavel pelo acesso ao banco de dados"""

	def __init__(self):
		self._nome_db = 'sa.db'
		self._cadastros_tb = 'cadastros'
		self._partidas_tb = 'partidas'
		super(GerenteDB, self).__init__()


	def cria_db(self):
		"""Cria a DB e as tabelas, se nao existirem """
		conn = sqlite3.connect(self._nome_db)
		cursor = conn.cursor()

		cursor.execute("""
		CREATE TABLE IF NOT EXISTS %s(
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			nome TEXT NOT NULL,
			cor INTEGER NOT NULL,
			mac TEXT NOT NULL
		);
		""" % self._cadastros_tb)

		cursor.execute("""
		CREATE TABLE IF NOT EXISTS %s(
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			data TEXT NOT NULL,
			hora TEXT NOT NULL,
			roboA TEXT NOT NULL,
			cacasA INTEGER,
			roboB TEXT NOT NULL,
			cacasB INTEGER
		);
		""" % self._partidas_tb)

		conn.close()


	def cadastra_robo(self, nome, cor, mac):
		"""Salva um cadastro de robo """
		conn = sqlite3.connect(self._nome_db)
		cursor = conn.cursor()

		cursor.execute(("SELECT id FROM %s WHERE nome=?" % self._cadastros_tb), (nome,))
		if len(cursor.fetchall()):
			# Cadastro ja existe
			return -1


		cursor.execute(("""
		INSERT INTO %s (nome, cor, mac)
		VALUES (?,?,?)
		""" % self._cadastros_tb), (nome, cor, mac))

		conn.commit()
		conn.close()
		return 0


	def salva_partida(self, robo_a, cacas_a, robo_b, cacas_b):
		"""Salva uma partida no DB (historico)
		Adiciona data e hora ao sql """
		conn = sqlite3.connect(self._nome_db)
		cursor = conn.cursor()

		data = datetime.now()
		data_str = "%d-%d-%d" % (data.year, data.month, data.day)
		hora_str = "%d:%d:%d" % (data.hour, data.minute, data.second)

		cursor.execute(("""
		INSERT INTO %s (data, hora, roboA, cacasA, roboB, cacasB)
		VALUES (?,?,?,?,?,?)
		""" % self._partidas_tb), (data_str, hora_str, robo_a, cacas_a, robo_b, cacas_b))

		conn.commit()
		conn.close()


	def get_geral(self, tabela):
		"""Select generico no DB: 'select * from tabela' """
		conn = sqlite3.connect(self._nome_db)
		cursor = conn.cursor()

		cursor.execute("SELECT * FROM %s;" % tabela)
		ret = cursor.fetchall()
		conn.close()

		return ret


	def _monta_dicionario_cadastro(self, cadastros_db):
		"""Monta dicionarios a partir dos cadastros salvos no banco
		Retorna uma lista com esses dicionarios (cadastros)
		Caso nao tenha nenhum cadastro, retorna lista vazia"""
		cadastros = []
		for cadastro in cadastros_db:
			c = {'id': cadastro[0]}
			c['nome'] = cadastro[1]
			c['cor'] = cadastro[2]
			c['mac'] = cadastro[3]
			cadastros.append(c)

		return cadastros


	def get_cadastros(self):
		"""Retorna uma lista com os cadastros existentes no banco"""
		cadastros_db = self.get_geral(self._cadastros_tb)
		return self._monta_dicionario_cadastro(cadastros_db)


	def get_cadastro(self, nome):
		"""Get em um cadastro especifico (busca pelo nome)
		Retorna uma lista vazia, caso o cadastro nao exista """
		conn = sqlite3.connect(self._nome_db)
		cursor = conn.cursor()

		cursor.execute(("SELECT * FROM %s WHERE nome=?;" % self._cadastros_tb), nome)
		cadastro = self._monta_dicionario_cadastro(cursor.fetchall())
		conn.close()

		return cadastro


	def get_partidas(self):
		"""Retorna uma lista de dicionarios (partidas) - historico"""
		partidas_db = self.get_geral(self._partidas_tb)
		partidas = []
		for partida in partidas_db:
			p = {'id': partida[0]}
			p['data'] = partida[1]
			p['hora'] = partida[2]
			p['robo_a'] = partida[3]
			p['cacas_a'] = partida[4]
			p['robo_b'] = partida[5]
			p['cacas_b'] = partida[6]
			partidas.append(p)

		return partidas

'''
### TESTE:

if __name__ == '__main__':
	print("Criando DB ...")
	gerente_db = GerenteDB()
	gerente_db.cria_db()

	for i in range(1, 3):
		print("\nCadastrando %dº robo" % i)
		try:
			nome = input("Nome: ")
			cor = int(input("Cor (int): "))
			mac = input("MAC: ")
		except:
			print("Invalido")
			exit()

		gerente_db.cadastra_robo(nome, cor, mac)

	print("\nSalvando historico")
	try:
		roboA = input("Primeiro robo: ")
		roboB = input("Segundo robo: ")
		cacasA = int(input("Cacas encontradas primeiro robo (int): "))
		cacasB = int(input("Cacas encontradas segundo robo (int): "))
	except:
		print("Invalido")
		exit()

	gerente_db.salva_partida(roboA, cacasA, roboB, cacasB)

	print("\nExibindo cadastros ... ")
	cadastros = gerente_db.get_cadastros()
	for cadastro in cadastros:
		print(cadastro)

	print("\nExibindo partidas ... ")
	partidas = gerente_db.get_partidas()
	for partida in partidas:
		print(partida)
'''