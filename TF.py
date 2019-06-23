# Nomes: Gustavo Duarte

import sys
from collections import defaultdict
path = sys.argv[1]
# funcao que le o arquivo txt e faz o parse para o automato 
def define_automaton(automato):
    linha = automato.split(';')
    estados, simbolos, inicial, finais = linha
    estados = estados.replace("M=({", '').replace('}', '')
    estados = estados.split(',')
    simbolos = simbolos.replace('{', '').replace('}', '')
    simbolos = simbolos.split(',')
    finais = finais.replace('{', '').replace("})", '')

    return estados, simbolos, inicial, finais
# funcao que reconhece palavras 
def recAccepts(transicoes, estado, aceitacao, palavra, i, bools):
    for j in range(len(palavra)):
        if palavra[j] not in transicoes[estado].keys():
            break
        for each in transicoes[estado][palavra[j]]: #verifico todas as possibilidades
            estado = each
            if j == len(palavra)-1 and estado in aceitacao: #o último símbolo é lido e o estado atual está no conjunto de estados finais
                bools.append("V")
            recAccepts(transicoes, estado, aceitacao, palavra[i+1:], i, bools) #string de entrada para a próxima transição é input [i + 1:]
        i = i+1
    if "V" in bools:
        return True
    else:
        return False        

with open(path) as file:
    linhas = []
    for linha in file:
        linhas.append(linha)
    automato = linhas[0]
    estados, simbolos, inicial, finais = define_automaton(automato)
    myDict = defaultdict(dict)
    for i in range(len(linhas)):
        transicao = linhas[i]
        de = transicao[1:3]
        presença = transicao[4:5]
        para = transicao[7:9]
        myDict[de].setdefault(presença, []).append(para)
    #ACEITA:
	#tive que substituir as letras que teriam 2 palavras no parse ou seja
	# co ficou o RE ficou e e o Ca ficou F
    print("ACEITA:")
    print()
    print(recAccepts(myDict, inicial, finais, "O", 0, []))       #Compra  um filme.
    print(recAccepts(myDict, inicial, finais, "OD", 0, []))      #Compra um filme e depois doa para um usuario.
    print(recAccepts(myDict, inicial, finais, "RFO", 0, []))     #Reserva um filme depois confirma a reserva e depois compra.
    print(recAccepts(myDict, inicial, finais, "A", 0, []))       #Aluga um filme direto
    print(recAccepts(myDict, inicial, finais, "AEA", 0, []))     #Aluga um filme e depois renova o filme e aluga.
    
    #REJEITA:
    print("REJEITA:")    
    print()    
    print(recAccepts(myDict, inicial, finais, "R", 0, []))       #Só reserva um filme.
    print(recAccepts(myDict, inicial, finais, "RC", 0, []))      #Reserva um filme e depois cancela
    print(recAccepts(myDict, inicial, finais, "AE", 0, []))      #Aluga um filme e depois renova o filme sem confirmar o aluguel.
    print(recAccepts(myDict, inicial, finais, "RCAE", 0, []))	 #Reserva um filme depois cancela e aluga o filme e depois fica numa nova reserva.
    print(recAccepts(myDict, inicial, finais, "RFE", 0, []))     #Reserva e confirma a reserva e depois fica na reserva do filme novamente.
    
    print("Faça testes om diversas entradas, e se quiser sair digite EXIT:")
    
    test = ""
    while test != "SAIR":
        test = input("Digite uma palavra a ser testada: ")
        if test == "SAIR":
            sys.exit()
        print(recAccepts(myDict, initial, finals, test, 0, []))

