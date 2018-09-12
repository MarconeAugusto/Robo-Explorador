from projetoRobo import Movimento

class Manual:
	
	def setAtualizaPosicao(direcao): #utilizado para informar qual movimento o robô deve fazer
		return Movimento.move(direcao)
		
	def getPosicaoAtual():#utilizado para validar caças
		return Movimento.getPosicaoAtual()
