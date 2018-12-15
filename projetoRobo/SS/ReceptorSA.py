import pika
import json
from threading import Thread

from projetoRobo.SS import compartilhados
from copy import deepcopy
import time


class ReceptorSA(Thread):

    def __init__(self, host):
        print("Iniciando RabbitMQ receptor..")
        super(ReceptorSA, self).__init__()
        self._nome = "g2"
        self._exchange = 'SA_to_SS'

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(host)))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self._exchange, exchange_type='direct')

        result = self.channel.queue_declare(exclusive=True)
        self._queue_name = result.method.queue

        self.channel.queue_bind(exchange=self._exchange, queue=self._queue_name, routing_key=self._nome)

        self.channel.basic_consume(self.trata_msg_recebida, queue=self._queue_name, no_ack=True)

    def trata_msg_recebida(self, ch, method, properties, body):
        try:
            msg = json.loads(body)
        except:
            return

        print("RECEBENDO DO SA")
        # Identificador (indica que a msg veio do SS)
        msg['_dir'] = 'sa'

        with compartilhados.sw_lock:
            # Copia a mensagem para o buffer de transmissao
            foo = deepcopy(msg)
            if 'jogadorA' in msg:

                if msg['jogadorA'] == self.robo:
                    foo = {'_dir': 'sa', 'cmd': 1100, 'modo_jogo': msg['modo_jogo'],
                           'cacas': msg['cacas'], 'x': msg['xA'], 'y': msg['yA']}

                elif msg['jogadorB'] == self.robo:
                    foo = {'_dir': 'sa', 'cmd': 1100, 'modo_jogo': msg['modo_jogo'],
                           'cacas': msg['cacas'], 'x': msg['xB'], 'y': msg['yB']}

                with compartilhados.sacomrx:
                    compartilhados.sw_msg = deepcopy(foo)
                    # Chama o gerente
                    compartilhados.sw_event.set()
                    # Tempo de seguranca para o gerente pegar a msg
                    time.sleep(0.2)

            else:

                with compartilhados.sacomrx:
                    compartilhados.sw_msg = deepcopy(msg)
                    # Chama o gerente
                    compartilhados.sw_event.set()
                    # Tempo de seguranca para o gerente pegar a msg
                    time.sleep(0.2)

            compartilhados.sw_event.clear()

    def run(self):
        self.channel.start_consuming()