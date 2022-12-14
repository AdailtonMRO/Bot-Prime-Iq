from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from getpass import getpass
from colorama import init, Fore, Back
import logging
import configparser
import sys
import json
import requests
from time import sleep
import os
from threading import Thread, Lock
import time

logging.disable(level=(logging.DEBUG))


init(convert=True, autoreset=True)



def perfil():
	perfil = json.loads(json.dumps(API.get_profile_ansyc()))
	return perfil['result']

def banca():
    return API.get_balance()

def stop(lucro, win, loss):
    if lucro <= float('-' + str(abs(loss))):
    	print(Fore.RED + ' META DE STOP LOSS BATIDO!\n')
    	input('\n APERTE ENTER PARA SAIR.')
    	sys.exit()

    if lucro >= float(abs(win)):
        print(Fore.GREEN + ' META DE STOP WIN BATIDO!\n')
        input('\n APERTE ENTER PARA SAIR.')
        sys.exit()

def Martingale(valor, payout):
	lucro_esperado = valor * payout
	perca = float(valor)	
		
	while True:
		if round(valor * payout, 2):
			return round(valor * 2)
			break
		valor += 0.01

def Payout(par):
	API.subscribe_strike_list(par, 1)
	while True:
		d = API.get_digital_current_profit(par, 1)
		if d != False:
			d = round(int(d) / 100, 2)
			break
		time.sleep(1)
	API.unsubscribe_strike_list(par, 1)
	
	return d

print(Fore.BLUE +'''
-----------------------------------------------------------------------------
|      _______  _______ _________ _______  _______   _________ _______      |
|     (  ____ )(  ____ )\__   __/(       )(  ____ \  \__   __/(  ___  )     |
|     | (    )|| (    )|   ) (   | () () || (    \/     ) (   | (   ) |     |
|     | (____)|| (____)|   | |   | || || || (__         | |   | |   | |     |
|     |  _____)|     __)   | |   | |(_)| ||  __)        | |   | |   | |     |
|     | (      | (\ (      | |   | |   | || (           | |   | | /\| |     |
|     | )      | ) \ \_____) (___| )   ( || (____/\  ___) (___| (_\ \ |     |
|     |/       |/   \__/\_______/|/     \|(_______/  \_______/(____\/_)     |
|                                                                           | 
-----------------------------------------------------------------------------                                                               
''')
print(Fore.RED +'''  Todas as estrat??gias e investimentos envolvem risco de perda. 
  Nenhuma informa????o contida neste produto deve ser interpretada como uma garantia de resultados.\n''')
print(' -----------------------------')
print(' -----------------------------')
print(' OL??, SEJA BEM-VIDO AO PRIME IQ!')
print(Back.RED +''' VERFIQUE SE O REL??GIO DE SEU PC EST?? SINCRONIZADO COM A DA IQ OPTION.''')
print(' -----------------------------')
print(' -----------------------------')
print(Back.BLUE +' POR SEGURAN??A SUA SENHA ESTAR?? INVIS??VEL.')
API = IQ_Option(input(' DIGITE SEU EMAIL: '),getpass(' DIGITE SUA SENHA DA IQ: '))
print(' -----------------------------')
print(' -----------------------------')
print(Fore.YELLOW +' CHECANDO DADOS...')
API.connect()
if API.check_connect():
	print(Fore.GREEN +' VOC?? CONECTOU COM SUCESSO!')
else:
	print(Fore.RED +' ERRO AO CONECTAR.')
	input('\n\n APERTE ENTER PARA SAIR E ABRA NOVAMENTE.')
	sys.exit()

def perfil():
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))
    return perfil
	#--- end perfil
	# chama a fun????o e salva o retorno em uma variavel x
x = perfil()
	# imprime somente o campo informado

print(' SEU ID:', x['user_id'])
print(' BEM VINDO(A):', x['name'])
print(' ---------------------------')
print(' ---------------------------')
API.change_balance(input(' ESCOLHA OPERAR EM PRACTICE OU REAL (ESCREVA APENAS EM MAI??SCULO): '))
print(' ---------------------------')
print(' ---------------------------')
print(Back.GREEN +''' SUA BANCA: $''',banca())
print(' ---------------------------')
print(' ---------------------------')

while True:
	try:
		operacao = int(input(' DIGITE O N??MERO 1 E APERTE ENTER): \n\n  1-) DIGITAL\n  R.: '))
			
		if operacao > 0 and operacao < 3 : break
	except:
		print(Fore.RED + '\n OP????O INEXISTENTE.')

pares = API.get_all_open_time()
print(' ---------------------------')
print(' ---------------------------')

def payout(par, tipo, timeframe = 5):
	if tipo == 'turbo':
		a = API.get_all_profit()
		return int(100 * a[par]['turbo'])
		
	elif tipo == 'digital':
	
		API.subscribe_strike_list(par, timeframe)
		while True:
			d = API.get_digital_current_profit(par, timeframe)
			if d != False:
				d = int(d)
				break
			time.sleep(1)
		API.unsubscribe_strike_list(par, timeframe)
		return d

if operacao == 1:
	print(' PARIDADES ABERTAS NA DIGITAL: \n')
	for paridade in pares['digital']:
		if pares['digital'][paridade]['open'] == True:
			print(' ',paridade+' | PAYOUT: '+str(payout(paridade, 'digital')))
print(' -----------------------------')
print(' -----------------------------')
par = input(' COLOQUE UMA PARIDADE PARA OPERAR (EX.: EURJPY) SE FOR EM OTC COLOQUE "-OTC" NO FINAL: ').upper()
print(' -----------------------------')
print(' -----------------------------')
while True:
	try:
		estrategia = int(input(' QUAL ESTRAT??GIA UTILIZAR? \n\n  [1] MHI DE MEIO CICLO (O PADR??O ?? MINORIA)\n  [2] MHI 1\n  [3] MHI 2\n  [4] MHI 3\n  [5] TR??S VIZINHOS (O PADR??O ?? MAIORIA)\n  [6] FIVEFLIP (O PADR???? ?? MINORIA)\n  [7] MILH??O\n  [8] TORRE G??MEAS (O PADR??O ?? MAIORIA)\n   R.: '))
			
		if estrategia > 0 and estrategia < 9 : break
	except:
		print(Fore.RED + '\n OP????O INEXISTENTE.')
print(' -----------------------------')
print(' -----------------------------')
while True:
	try:
		alternativa = int(input(' ESCOLHA OPERAR ENTRE MAIORIA OU MINORIA (DIGITE O N??MERO DE UMA DAS OP????ES E APERTE ENTER) :\n  1-) MINORIA\n  2-) MAIORIA\n  R.: '))
			
		if alternativa > 0 and alternativa < 3 : break
	except:
		print(Fore.RED + '\n OP????O INEXISTENTE.')
print(' -----------------------------')
print(' -----------------------------')
valor_entrada = float(input(' COLOQUE O VALOR DA SUA ENTRADA: '))
valor_entrada_b = float(valor_entrada)
print(' -----------------------------')
print(' -----------------------------')
stop_loss = float(input(' COLOQUE SUA META DE STOP LOSS: '))
print(' -----------------------------')
print(' -----------------------------')
stop_win = float(input(' COLOQUE SUA META DE STOP WIN: '))
print(' -----------------------------')
print(' -----------------------------')
martingale = int(input(' QUANTOS MARTINGALES? : '))
martingale += 1
print(' -----------------------------')
print(' -----------------------------')
print(Fore.YELLOW + ' CARREGANDO CONFIGURA????ES...')
print(' -----------------------------')
print(' -----------------------------')
lucro = 0
payout = Payout(par)
while True:
		minutos = float(((datetime.now()).strftime('%M.%S')))
		if estrategia == 1 : #MHI - Meio Ciclo
			entrar = True if (minutos == 14.58 and minutos <= 15) or (minutos >= 29.58 and minutos <= 30) or (minutos >= 44.58 and minutos <= 45) or minutos == 59.58 else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE H?? PADR??O NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )
				
		if estrategia == 2 : #MHI
			entrar = True if (minutos == 29.58 and minutos <= 30) or minutos >= 59.58 else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE H?? PADR??O NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 3 : #MHI 2
			entrar = True if (minutos == 4.58 and minutos <= 5) or (minutos >= 34.58 and minutos <= 35) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE H?? PADR??O NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 4 : #MHI 3
			entrar = True if (minutos == 9.58 and minutos <= 10) or (minutos >= 39.58 and minutos <= 40) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE H?? PADR??O NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 5 : #Tr??s Vizinhos
			entrar = True if (minutos == 19.58 and minutos <= 20) or (minutos >= 49.58 and minutos <= 50) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE H?? PADR??O NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 6 : #FiveFlip
			entrar = True if (minutos == 24.58 and minutos <= 25) or (minutos >= 54.58 and minutos <= 55) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE H?? PADR??O NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 7 : #Milh??o
			entrar = True if (minutos == 19.58 and minutos <= 20) or (minutos >= 49.58 and minutos <= 50) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE H?? PADR??O NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 8 : #Torre G??meas
			entrar = True if (minutos == 24.58 and minutos <= 25) or (minutos >= 54.58 and minutos <= 55) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE H?? PADR??O NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if entrar :
			print('\n\n PRONTO, HORA DE OPERAR!')
			print(' -----------------------')
			dir = False
			print(' VERIFICANDO AS VELAS... ', end='')
			if estrategia == 1: #MHI - Meio Ciclo
				velas = API.get_candles(par, 300, 3, time.time())

				velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
				velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
				velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
							
					
				cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]		
				print(cores)

			if estrategia == 2: #MHI
				velas = API.get_candles(par, 300, 3, time.time())

				velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
				velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
				velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
							
					
				cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]		
				print(cores)

			if estrategia == 3: #MHI 2
				velas = API.get_candles(par, 300, 4, time.time())

				velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
				velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
				velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
				velas[3] = 'g' if velas[3]['open'] < velas[3]['close'] else 'r' if velas[3]['open'] > velas[3]['close'] else 'd'
							
					
				cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]		
				print(cores)

			if estrategia == 4: #MHI 3
				velas = API.get_candles(par, 300, 5, time.time())

				velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
				velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
				velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
				velas[3] = 'g' if velas[3]['open'] < velas[3]['close'] else 'r' if velas[3]['open'] > velas[3]['close'] else 'd'	
				velas[4] = 'g' if velas[4]['open'] < velas[4]['close'] else 'r' if velas[4]['open'] > velas[4]['close'] else 'd'
							
					
				cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]		
				print(cores)

			if estrategia == 5: #Tr??s Vizinhos
				velas = API.get_candles(par, 300, 1, time.time())

				velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
							
					
				cores = velas[0]	
				print(cores)

			if estrategia == 6: #FiveFlip
				velas = API.get_candles(par, 300, 1, time.time())

				velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
							
					
				cores = velas[0]	
				print(cores)

			if estrategia == 7: #Milh??o
				velas = API.get_candles(par, 300, 6, time.time())

				velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
				velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
				velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'	
				velas[3] = 'g' if velas[3]['open'] < velas[3]['close'] else 'r' if velas[3]['open'] > velas[3]['close'] else 'd'
				velas[4] = 'g' if velas[4]['open'] < velas[4]['close'] else 'r' if velas[4]['open'] > velas[4]['close'] else 'd'
				velas[5] = 'g' if velas[5]['open'] < velas[5]['close'] else 'r' if velas[5]['open'] > velas[5]['close'] else 'd'
					
				cores = velas[0]+ ' ' + velas[1]+ ' ' + velas[2]+ ' ' + velas[3]+ ' ' + velas[4]+ ' ' + velas[5]		
				print(cores)

			if estrategia == 8: #Torre G??meas
				velas = API.get_candles(par, 300, 6, time.time())

				velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
				velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
				velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'	
				velas[3] = 'g' if velas[3]['open'] < velas[3]['close'] else 'r' if velas[3]['open'] > velas[3]['close'] else 'd'
				velas[4] = 'g' if velas[4]['open'] < velas[4]['close'] else 'r' if velas[4]['open'] > velas[4]['close'] else 'd'
					
				cores = velas[0]		
				print(cores)
				
				#Minoria ou Maioria
			if cores.count('g') > cores.count('r') and cores.count('d') == 0 : dir = ('put' if alternativa == 1 else 'call')
			if cores.count('r') > cores.count('g') and cores.count('d') == 0 : dir = ('call' if alternativa == 1 else 'put')
				
			if dir:
				print(' DIRE????O DA OPERA????O: ',dir)
				print(' -----------------------')
				valor_entrada = valor_entrada_b
				for i in range(martingale):
				
					status,id = API.buy_digital_spot(par, valor_entrada, dir, 5) if operacao == 1 else API.buy(valor_entrada, par, dir, 5)
					
					if status:
						while True:
							try:
								status,valor = API.check_win_digital_v2(id) if operacao == 1 else API.check_win_v3(id)
							except:
								status = True
								valor = 0
							
							if status:
								valor = valor if valor > 0 else float('-' + str(abs(valor_entrada)))
								lucro += round(valor, 1)
								print(' RESULTADO DA OPERA????O: ', end='')
								print(Fore.GREEN + 'WIN $ ' if valor > 0 else Fore.RED + 'LOSS $ ' , round(valor, 1) ,'-> LUCRO: $', round(lucro, 1),('-> '+str(i)+ ' MARTINGALE' 
									if i > 0 else '' ))
								print(' -----------------------')
								valor_entrada = Martingale(valor_entrada, payout)

								stop(lucro, stop_win, stop_loss)
								
								break
							
						if valor > 0 : break
						
					else:
						print(Fore.RED + '\n N??O FOI POSS??VEL A OPERA????O!\n\n')

		time.sleep(0.1)
