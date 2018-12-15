import pika
import json
from threading import Thread, Event, Lock
from copy import deepcopy
from projetoRobo.SS import compartilhados


class TransmissorSA(Thread):

    def __init__(self, host):
        Thread.__init__(self)
        print("Iniciando RabbitMQ transmissor..")
        #credentials = pika.PlainCredentials('robot1', 'robot1')
        #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, 5672, '/', credentials))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='SS_to_SA')

    def run(self):
        while True:
            print("SA")
            # Espera ate ter uma mensagem a transmitir
            compartilhados.sa_event.wait()
            print("foi pro SA")

            # Bloqueia enquanto a mensagem e enviada
            #with compartilhados.lock:
            msg = deepcopy(compartilhados.sa_msg)

            print(msg)

            try:
                msg = json.dumps(msg)
                self.channel.basic_publish(exchange='',
                                           routing_key='SS_to_SA',
                                           body=msg)
            except:
                pass

            compartilhados.sa_event.clear()

        self.connection.close()