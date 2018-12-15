from threading import Thread, Event, Lock

class Distributor():


    def __init__(self, robo):
        self._robo = robo
        self.mac = ''

        self.validar = False

        self.obstaculo = False

        self.mensagem = ''

        self.x = 0
        self.y = 0

    def getNome(self):
        return self._robo

    def getCoord(self):
        return self.x, self.y

    def getY(self):
        return self.y

    def getValidacao(self):
        return self.validar

    def getObstaculo(self):
        return self.obstaculo

    def setMensagem(self, msg):
        self.mensagem = msg

    def getMensegem(self):
        return self.mensagem

    def setMac(self, mac):
        self.mac = mac

    def getMac(self):
        return self.mac

    def setValidacao(self, validacao):
        self.validar = validacao

    def setCoord(self, x, y):
        self.x = x
        self.y = y