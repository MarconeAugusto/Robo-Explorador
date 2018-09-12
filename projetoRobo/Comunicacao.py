from projetoRobo import *

class Comunicacao:
	
	#Inicialização
	def getEndMac():
		return Inicializacao.getEndMac()
		
	def setCorLed(corLed):
		return Inicializacao.setCorLed(corLed)
		#garantir na classe Inicialização que vai dar certo !!!!!!!!!! 
				
	def modoJogo(modo):
		return Inicializacao.modoJogo(modo)
		
	def setPosicaoInicial(pos):  # setPosicao()
		return Inicializacao.setPosicaoInicial(pos)
				
	def inicaJogo():
		return Inicializacao.inicaJogo()
		
		
		
	#Modo Autônomo
	def setAtualizaPosicao(posAtual, posProx):
		return Autonomo.setAtualizaPosicao(posAtual, posProx)
		
	def getAtualizaPosicaoAdv():
		return Autonomo.setAtualizaPosicao()
				
	def setAtualizaPosicaoAdv(posAdv):
		return Autonomo.setAtualizaPosicaoAdv(posAdv)
				
	def getAtualizaCacas():
		return Autonomo.getAtualizaCacas()
			
	def setAtualizaCacas(listaCacas):
		return Autonomo.setAtualizaCacas(listaCacas)
				
	def setPausa():
		return Autonomo.setPausa()
				
	def setFimDeJogo():
		return Autonomo.setFimDeJogo()
				
	#Modo Manual
	def setAtualizaPosicao(direcao): #testar conflito
		return Manual.setAtualizaPosicao(direcao)
		
	def getPosicaoAtual():#utilizado para validar caças
		return Manual.getPosicaoAtual()
		
	
