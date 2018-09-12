from projetoRobo import Movimento

class Manual:
	
	def setAtualizaPosicao(direcao): #utilizado para informar qual movimento o robô deve fazer
		return Movimento.vira(direcao) # alterar o nome vira para move
		
	def getPosicaoAtual():#utilizado para validar caças
		return Movimento.getPosicaoAtual()
