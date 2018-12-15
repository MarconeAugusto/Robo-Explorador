#!/usr/bin/env python3
# coding: utf-8
from threading import Thread

#from projetoRobo.SS.SS import PrincipalSS
#from projetoRobo.SS.clienteSR import *
from projetoRobo.SS.Mensagens import *
from projetoRobo.SS.TransmissorSA import *
from projetoRobo.SS.ReceptorSA import *
from copy import deepcopy
from projetoRobo.SS import compartilhados, InterfaceGrafica
from projetoRobo.SS.Distributor import *
from projetoRobo.SS.ComunicacaoSR import *
from projetoRobo.SS.SS import *
import time

class ClienteSR:
    def setCorLed(self, corLED):
        ns = Pyro4.locateNS("10.42.0.79")  # IP do robô
        uri = ns.lookup('ServidorSR')
        print(uri)
        o = Pyro4.Proxy(uri)
        return o.setCorLed(corLED)

    def getEndMAC(self):
        ns = Pyro4.locateNS("10.42.0.79")  # IP do robô
        uri = ns.lookup('ServidorSR')
        print(uri)
        o = Pyro4.Proxy(uri)
        return o.getEndMAC()

    ##acessada via interface gráfica
    def MovimentoManual(self, direcao):
        ns = Pyro4.locateNS("10.42.0.79")  # IP do robô
        uri = ns.lookup('Movimento')
        print(uri)
        try:
            o = Pyro4.Proxy(uri)
            if PrincipalSS.getEstadoDoJogo(self):
                o.move(direcao)
            else:
                print("JOGO PAUSADO!")
        except Exception:
            print("Pyro traceback:")
            print("".join(Pyro4.util.getPyroTraceback()))

    ##acessada via interface gráfica
    def MovimentoAutonomo(self):
        print("Iniciando movimento Autônomo")
        ns = Pyro4.locateNS("10.42.0.79")  # IP do robô
        uri = ns.lookup('Movimento')
        print(uri)
        try:
            o = Pyro4.Proxy(uri)
            o.modoJogo(1)
        except Exception:
            print("Pyro traceback:")
            print("".join(Pyro4.util.getPyroTraceback()))

class Switch(Thread):
    compartilhados.init()

    def __init__(self, dist):
        Thread.__init__(self)

        self.distributor = "g2"

        c = ClienteSR()

        self.srCOM = Comunicacao()
        mac = c.getEndMAC()
        print("Mac: " ,mac)
        ##self.distributor.setMac(mac)
        ##self.srCOM.rx()

        self.tx = TransmissorSA('localhost')
        self.tx.start()

        #self.rx = ReceptorSA('localhost', self.distributor.getNome())
        self.rx = ReceptorSA('localhost')
        print("iniciando receptor")
        self.rx.start()

    def _envia_msg_sa(self, msg):
         with compartilhados.sa_lock:
            compartilhados.sa_msg = msg
            compartilhados.sa_event.set()

    def _envia_msg_sr(self, msg):
        #with compartilhados.lock:
        #    compartilhados.msg = msg
        #    compartilhados.sr_event.set()
        self.srCOM.enviar(self.srCOM.getRobo(), msg)

    def _avisa_autonomo(self, msg):
        with compartilhados.autonomo_lock:
            compartilhados.autonomo_msg = msg
            compartilhados.autonomo_event.set()
        print("msg do avisa:")

    def _avisa_main(self, msg):
        with compartilhados.main_lock:
            compartilhados.main_msg = msg
            compartilhados.main_event.set()

    def run(self): #mensagens recebidas do SA
        #lista = 'lista|12/22/23'
        while True:
            ##print("Teste")
            compartilhados.sw_event.wait()

            with compartilhados.sw_lock:
                msg = deepcopy(compartilhados.sw_msg)
                print("Mensagem SA: ",msg)
                print(msg['modo_jogo'])

                if msg['_dir'] == 'sa':
                    # Mensagens Vinda do SA
                    if 'cmd' not in msg:
                        compartilhados.sw_event.clear()
                        continue

                    cmd = msg['cmd']
                    if cmd == SA_to_SS.ValidacaoCaca:
                        if msg['ack'] == 1:
                            self.distributor.setValidacao(True)
                            msg = {'cmd': SS_to_SS.ValidaCaca_resp, 'caca': 1}
                            self._avisa_main(msg)

                        else:
                            self.distributor.setValidacao(False)
                            msg = {'cmd': SS_to_SS.ValidaCaca_resp, 'caca': 0}
                            self._avisa_main(msg)

                        #msg = {'cmd': SS_to_SR.ValidaCaca}
                        #self._envia_msg_sr(msg)

                    elif cmd == SA_to_SS.AtualizaMapa:
                        pass

                    elif cmd == SA_to_SS.CadastraRobo:
                        pass

                    elif cmd == SA_to_SS.Continua:
                        pass

                    elif cmd == SA_to_SS.Pausa:
                        pass

                    elif cmd == SA_to_SS.FimJogo:
                        pass

                    elif cmd == SA_to_SS.NovoJogo:
                        print("Novo jogo")
                        if msg['modo_jogo'] == 2:
                            print("Modo Autonomo")
                            # Create new threads
                            thread2 = InterfaceGrafica.Configuracao(2)  # inicia servidor Pyro4 do SS
                            thread3 = InterfaceGrafica.Configuracao(3)  # inicia interface Autonomo , alterar depois
                            thread4 = InterfaceGrafica.Configuracao(4)  # Registra o servidor de nomes
                            # Start new Threads
                            thread2.start()
                            time.sleep(1)
                            thread3.start()
                            thread4.start()
                            time.sleep(1)
                            ClienteSR.MovimentoAutonomo(self)

                            #coord = msg['x'] + msg['y']

                            ## TRATAR AS CAÇAS
                            #self.srCOM.enviar(self.srCOM.getRobo(), msg['cacas'])
                            print()


                        elif msg['modo_jogo'] == 1:
                            #coord = msg['x'] + msg['y']
                            print("Modo Manual")
                            # Create new threads
                            thread1 = InterfaceGrafica.Configuracao(1)
                            thread2 = InterfaceGrafica.Configuracao(2)
                            thread4 = InterfaceGrafica.Configuracao(4)

                            # Start new Threads
                            thread1.start()
                            time.sleep(1)
                            thread2.start()
                            time.sleep(1)
                            thread4.start()


                elif msg['_dir'] == 'ss':
                    # Mensagens Vinda do Ss
                    if 'cmd' not in msg:
                        compartilhados.sw_event.clear()
                        continue

                    elif msg['cmd'] == SS_to_SS.ValidaCaca:
                        msg = {'_dir': 'ss', '_robo': self.distributor.getNome(),
                               'cmd': SS_to_SA.ValidaCaca, 'x': msg['x'], 'y': msg['y']}
                        self._envia_msg_sa(msg)




                elif msg['_dir'] == 'sr':
                    # Mensagens vindas do robo
                    msg = msg['cmd'].split("|")
                    cmd = msg[0]
                    robo = self.distributor.getNome()


                    if cmd == "destino":
                        x = int(msg[1][0])
                        y = int(msg[1][1])
                        msg = {'_dir':'sa', '_robo': robo, 'cmd': SS_to_SA.MovendoPara, 'x': x, 'y': y}
                        self.distributor.setCoord(x, y)
                        self._avisa_autonomo({'cmd':SS_to_SS.MovendoPara})
                        self._envia_msg_sa(msg)



                    elif cmd == "validar":
                        x = int(msg[1][0])
                        y = int(msg[1][1])
                        msg = {'robo': robo, 'cmd': SS_to_SA.ValidaCaca, 'x': x, 'y': y}

                        self._avisa_autonomo({'cmd':SS_to_SS.ValidaCaca})
                        self._envia_msg_sa(msg)

                        #print('SA VALIDANDO CAÇA')
                        #time.sleep(2)
                        #print('Caça validada')
                        #self.srCOM.enviar(self.srCOM.getRobo(), 'validada'+'|'+'22/23')

                    elif cmd == "posAtual":
                        x = int(msg[1][0])
                        y = int(msg[1][1])
                        msg = {'robo': robo, 'cmd': SS_to_SA.PosicaoAtual, 'x': x, 'y': y}
                        self._envia_msg_sa(msg)
                        self._avisa_autonomo(msg)
                        self.srCOM.enviar(self.srCOM.getRobo(), lista)

                    elif cmd == "mac":
                        print("Recebendo MAC:", msg[1])
                        self.distributor.setMac(msg[1])

                    elif cmd == "uri":
                        msg = {'modo':'manual', 'uri': msg[1]}
                        self._avisa_main(msg)

                    elif cmd == "manual":
                        self.srCOM.enviar(self.srCOM.getRobo(), '00')
                        self.srCOM.enviar(self.srCOM.getRobo(), 'manual')

                    else:
                        return

                else:

                    msg = {'modo': 'auto'}

                    self._avisa_main(msg)
                    self.srCOM.enviar(self.srCOM.getRobo(), '00')
                    self.srCOM.enviar(self.srCOM.getRobo(), msg['modo'])
                    self.srCOM.enviar(self.srCOM.getRobo(), lista)



                compartilhados.sw_event.clear()