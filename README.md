# Projeto Integrador II - LEGO Mindstorms EV3

#### Grupo 2

* Ameliza Souza Corrêa
* Marcone Augusto de Paula Louzada
* Yan Lucas Martins



Este projeto foi desenvolvido na disciplina de Projeto Integrador II. Que consiste em desenvolver um robô que seja capaz de encontrar caças em um tabuleiro, bem como estar sempre se comunicando com um sistema externo, denominado Sistema Supervisório (SS), de onde receberá e enviará informações. Tais como instruções de novas direções, atualização de coordenadas e lista de caças.

Por sua vez, o SS, deverá tratar essas informações e enviá-las ao Sistema de Auditoria (SA). O SA, fica responsável por todo o controle da partida. Coletando e enviando dados para os SS's de todos os robôs envolvidos no jogo.



### Execução do projeto

Primeiramente, deve-se iniciar o sistema do robô (SR). Para isso, dentro da pasta SR, altere os IPs contidos nos arquivos a seguir, para o IP que será utilizado no SS:

* Autonomo.py
* ServidorSR.py

Em seguida, inicie o servidor Pyro4 e execute o arquivo Menu.py contido nessa mesma pasta:

```
pyro4 --host ip_do_robo
python3 Menu.py
```



Após isso será necessário iniciar o SS. Para isto, deve-se apenas executar o arquivo SS.py:

```
python3 SS.py
```



O SA deve, também, estar em execução, sendo necessário realizar o cadastro dos robôs através da inrerface.

* Esta etapa não foi completamente integrada com o SS contido neste projeto, no entanto, pode-se realizar a transmissão da posição inicial, lista de caças e cadastro do robô.

No arquivo test.py ao executá-lo, selecione a opção 1 para o cadastro do robô e a opção 5 para o início de um novo jogo.
