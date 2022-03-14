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

print(' -----------------------------')
print(' -----------------------------')
print(' OLÁ, SEJA BEM-VIDO AO PRIME IQ!')
print(Back.RED +''' VERFIQUE SE O RELÓGIO DE SEU PC ESTÁ SINCRONIZADO COM A DA IQ OPTION.''')
print(' -----------------------------')
print(' -----------------------------')

print(Back.BLUE +' POR SEGURANÇA SUA SENHA ESTARÁ INVISÍVEL.')
API = IQ_Option(input(' DIGITE SEU EMAIL: '),getpass(' DIGITE SUA SENHA DA IQ: '))
print(' -----------------------------')
print(' -----------------------------')
print(Fore.YELLOW +' CHECANDO DADOS...')
API.connect()
if API.check_connect():
	print(Fore.GREEN +' VOCÊ CONECTOU COM SUCESSO!')
else:
	print(Fore.RED +' ERRO AO CONECTAR.')
	input('\n\n APERTE ENTER PARA SAIR E ABRA NOVAMENTE.')
	sys.exit()

def perfil():
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))
    return perfil
	#--- end perfil
	# chama a função e salva o retorno em uma variavel x
x = perfil()
	# imprime somente o campo informado
print(' ---------------------------')
print(' ---------------------------')
print(' SEU ID:', x['user_id'])
print(' BEM VINDO(A):', x['name'])
print(' ---------------------------')
print(' ---------------------------')
while True:
	try:
		tipo_de_conta = int(input(' ESCOLHA O TIPO DE CONTA (DIGITE O NÚMERO DE UMA DAS OPÇÕES E APERTE ENTER): \n  1-) REAL\n  2-) TREINAMENTO\n  R.: '))
			
		if tipo_de_conta > 0 and tipo_de_conta < 3 : break
	except:
		print(Fore.RED + '\n OPÇÃO INEXISTENTE.')
	
	if tipo_de_conta == 1:
		API.change_balance('REAL')

	if tipo_de_conta == 2:
		API.change_balance('PRACTICE')
print(' ---------------------------')
print(' ---------------------------')
print(' SUA BANCA: $',banca())
print(' ---------------------------')
print(' ---------------------------')

while True:
	try:
		operacao = int(input(' VAI OPERAR EM QUAL? (DIGITE O NÚMERO DE UMA DAS OPÇÕES E APERTE ENTER): \n  1-) DIGITAL\n  2-) BINÁRIA\n  R.: '))
			
		if operacao > 0 and operacao < 3 : break
	except:
		print(Fore.RED + '\n OPÇÃO INEXISTENTE.')

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

if operacao == 2:
	print(' PARIDADES ABERTAS NA BINÁRIA: \n')
	for paridade in pares['turbo']:
		if pares['turbo'][paridade]['open'] == True:
			print(' ',paridade+' | PAYOUT: '+str(payout(paridade, 'turbo')))

par = input('\n COLOQUE UMA PARIDADE PARA OPERAR (EX.: EURJPY) SE FOR EM OTC COLOQUE "-OTC" NO FINAL: ').upper()

while True:
	try:
		estrategia = int(input('\n QUAL ESTRATÉGIA UTILIZAR? \n  [1] MHI DE MEIO CICLO \n  [2] MHI 1\n  [3] MHI 2\n  [4] MHI 3\n  [5] TRÊS VIZINHOS\n  [6] FIVEFLIP\n  [7] MILHÃO\n  [8] TORRE GÊMEAS\n  R.: '))
			
		if estrategia > 0 and estrategia < 9 : break
	except:
		print(Fore.RED + '\n OPÇÃO INEXISTENTE.')

while True:
	try:
		alternativa = int(input('\n ESCOLHA OPERAR ENTRE MAIORIA OU MINORIA (DIGITE O NÚMERO DE UMA DAS OPÇÕES E APERTE ENTER) :\n  1-) MINORIA\n  2-) MAIORIA\n  R.: '))
			
		if alternativa > 0 and alternativa < 3 : break
	except:
		print(Fore.RED + '\n OPÇÃO INEXISTENTE.')

valor_entrada = float(input('\n COLOQUE O VALOR DA SUA ENTRADA: '))
valor_entrada_b = float(valor_entrada)
stop_loss = float(input('\n COLOQUE SUA META DE STOP LOSS: '))
stop_win = float(input('\n COLOQUE SUA META DE STOP WIN: '))
martingale = int(input('\n QUANTOS MARTINGALES? : '))
martingale += 1
print(Fore.YELLOW + '\n CARREGANDO CONFIGURAÇÕES...')
lucro = 0
payout = Payout(par)
while True:
		minutos = float(((datetime.now()).strftime('%M.%S')))
		if estrategia == 1 : #MHI - Meio Ciclo
			entrar = True if (minutos == 14.58 and minutos <= 15) or (minutos >= 29.58 and minutos <= 30) or (minutos >= 44.58 and minutos <= 45) or minutos == 59.58 else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE HÁ PADRÃO NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )
				
		if estrategia == 2 : #MHI
			entrar = True if (minutos == 29.58 and minutos <= 30) or minutos >= 59.58 else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE HÁ PADRÃO NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 3 : #MHI 2
			entrar = True if (minutos == 4.58 and minutos <= 5) or (minutos >= 34.58 and minutos <= 35) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE HÁ PADRÃO NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 4 : #MHI 3
			entrar = True if (minutos == 9.58 and minutos <= 10) or (minutos >= 39.58 and minutos <= 40) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE HÁ PADRÃO NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 5 : #Três Vizinhos
			entrar = True if (minutos == 19.58 and minutos <= 20) or (minutos >= 49.58 and minutos <= 50) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE HÁ PADRÃO NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 6 : #FiveFlip
			entrar = True if (minutos == 24.58 and minutos <= 25) or (minutos >= 54.58 and minutos <= 55) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE HÁ PADRÃO NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 7 : #Milhão
			entrar = True if (minutos == 19.58 and minutos <= 20) or (minutos >= 49.58 and minutos <= 50) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE HÁ PADRÃO NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

		if estrategia == 8 : #Torre Gêmeas
			entrar = True if (minutos == 24.58 and minutos <= 25) or (minutos >= 54.58 and minutos <= 55) else False
			print(' TUDO CERTO! ESTOU VERIFICANDO SE HÁ PADRÃO NAS VELAS, POR FAVOR, AGUARDE...', end='\r' )

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

			if estrategia == 5: #Três Vizinhos
				velas = API.get_candles(par, 300, 1, time.time())

				velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
							
					
				cores = velas[0]	
				print(cores)

			if estrategia == 6: #FiveFlip
				velas = API.get_candles(par, 300, 1, time.time())

				velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
							
					
				cores = velas[0]	
				print(cores)

			if estrategia == 7: #Milhão
				velas = API.get_candles(par, 300, 6, time.time())

				velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
				velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
				velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'	
				velas[3] = 'g' if velas[3]['open'] < velas[3]['close'] else 'r' if velas[3]['open'] > velas[3]['close'] else 'd'
				velas[4] = 'g' if velas[4]['open'] < velas[4]['close'] else 'r' if velas[4]['open'] > velas[4]['close'] else 'd'
				velas[5] = 'g' if velas[5]['open'] < velas[5]['close'] else 'r' if velas[5]['open'] > velas[5]['close'] else 'd'
					
				cores = velas[0]+ ' ' + velas[1]+ ' ' + velas[2]+ ' ' + velas[3]+ ' ' + velas[4]+ ' ' + velas[5]		
				print(cores)

			if estrategia == 8: #Torre Gêmeas
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
				print(' DIREÇÃO DA OPERAÇÃO: ',dir)
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
								print(' RESULTADO DA OPERAÇÃO: ', end='')
								print(Fore.GREEN + 'WIN $ ' if valor > 0 else Fore.RED + 'LOSS $ ' , round(valor, 1) ,'-> LUCRO: $', round(lucro, 1),('-> '+str(i)+ ' MARTINGALE' 
									if i > 0 else '' ))
								print(' -----------------------')
								valor_entrada = Martingale(valor_entrada, payout)

								stop(lucro, stop_win, stop_loss)
								
								break
							
						if valor > 0 : break
						
					else:
						print(Fore.RED + '\n NÃO FOI POSSÍVEL A OPERAÇÃO!\n\n')

		time.sleep(0.1)