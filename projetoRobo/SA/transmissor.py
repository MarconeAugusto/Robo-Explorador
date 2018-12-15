import pika
import json
from threading import Thread, Event, Lock
import projetoRobo.SA.compartilhados
from projetoRobo.SA import compartilhados


class Transmissor(Thread):
	"""Classe transmissora de mensagens do sistema auditor."""

	def __init__(self, host):
		super(Transmissor, self).__init__()
		self._exchange = 'SA_to_SS'

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange=self._exchange, exchange_type='direct')

	def run(self):
		while True:
			# Espera ate ter uma mensagem a transmitir
			compartilhados.transmitir_event.wait()

			# Bloqueia enquanto a mensagem e enviada
			with compartilhados.transmitir_msg_lock:
				msg = compartilhados.transmitir_msg

				if '_dir' in msg: msg.pop('_dir')

				if '_robo' in msg:
					routing_key = msg['_robo']
					msg.pop('_robo')

					msg_prop = None
					if '_ttl' in msg:
						msg_prop = pika.BasicProperties(expiration=str(msg['_ttl']))
						msg.pop('_ttl')

					print("Transmitindo: %s" % str(msg))
					try:
						msg = json.dumps(msg)
						self.channel.basic_publish(exchange=self._exchange,
												   routing_key=routing_key,
												   body=msg,
												   properties=msg_prop)
					except:
						pass

				compartilhados.transmitir_event.clear()

		self.connection.close()