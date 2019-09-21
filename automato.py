import pprint
pp = pprint.PrettyPrinter(indent=4)


automato_teste1 = {
    'alfabeto': ['a', 'b'],
    'estInicial': 'q0',
    'estFinal': ['q2'],
    'transacoes': {
        'q0': {'a': 'q1', 'b': 'q3'},
        'q1': {'a': 'q3', 'b': 'q2'},
        'q2': {'a': 'q2', 'b': 'q2'},
        'q3': {'a': 'q3', 'b': 'q3'}
    }
}

automato_teste2 = {
    'alfabeto': ['a', 'b'],
    'estInicial': 'q0',
    'estFinal': ['q0', 'q4', 'q5'],
    'transacoes': {
        'q0': {'a': 'q2', 'b': 'q1'},
        'q1': {'a': 'q1', 'b': 'q0'},
        'q2': {'a': 'q4', 'b': 'q5'},
        'q3': {'a': 'q5', 'b': 'q4'},
        'q4': {'a': 'q3', 'b': 'q2'},
        'q5': {'a': 'q2', 'b': 'q3'}
    }
}

automato_teste3 = {
    'alfabeto': ['0', '1'],
    'estInicial': 'q0',
    'estFinal': ['q2', 'q3', 'q5'],
    'transacoes': {
        'q0': {'0': 'q1', '1': 'q3'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q5', '1': 'q4'},
        'q3': {'0': 'q5', '1': 'q4'},
        'q4': {'0': 'q4', '1': 'q4'},
        'q5': {'0': 'q5', '1': 'q4'}
    }
}


def instrucoes():
    instrucoes = "Para executar os algoritmos primeiro é necessário informar os dados do automato desejado."
    instrucoes += "\nDados necessários: alfabeto, estado inicial, estado final e transações. Seguir o modelo mostrado abaixo:"
    print(instrucoes)
    pp.pprint(automato_teste1)


def menu():
    while True:
        print('\n--------------------- MENU ---------------------')
        print('1 - Verificar se palavra é aceita pelo autômato')
        print('2 - Minimizar o autômato e mostrar estados equivalentes')
        print('3 - Sair')
        opcao = int(input('\nInforme a opção desejada: '))
        if opcao == 1:
            palavra = input('Informe a palavra para a verificação: ')
            print(verificarPalavra(palavra, automato_teste1))
        elif opcao == 2:
            estadosEquivalentes(automato_teste2)
        elif opcao == 3:
            print('Finalizando programa...')
            return
        else:
            print('Opção inválida!')


def verificarPalavra(palavra, automato):
    palavra = list(palavra)
    estadoAtual = automato['estInicial']
    for simb in palavra:
        if simb not in automato['alfabeto']:
            return 'Palavra contém elementos fora do alfabeto.'
        elif simb not in automato['transacoes'][estadoAtual]:
            return 'Está faltando transações.'

        estadoAtual = automato['transacoes'][estadoAtual][simb]

    return '\nA palavra foi aceita :)' if estadoAtual in automato['estFinal'] else '\nA palavra não foi aceita :('


def estadosEquivalentes(automato):
    # Construindo a tabela
    estados = [k for k in automato['transacoes'].keys()]
    tabela = dict()
    for k, v in enumerate(estados):
        if k != 0:
            tabela[v] = []
            for i in range(k):
                tabela[v].append('  ')
    last = estados.pop()

    # Preenchendo distinguíveis com base nos estados finais (linha)
    for k, v in tabela.items():
        if k in automato['estFinal']:
            for ind, v in enumerate(v):
                if estados[ind] in automato['estFinal']:
                    tabela[k][ind] = '  '
                else:
                    tabela[k][ind] = ' x'

    # Preenchendo distinguíveis com base nos estados finais (coluna)
    for k, v in enumerate(estados):
        if v in automato['estFinal']:
            for ch, val in tabela.items():
                if ch not in automato['estFinal'] and len(val) >= k:
                    val[k] = ' x'

    estados.append(last)
    for i in range(len(estados)):
        for k, v in tabela.items():
            par = []
            if i < len(v) and (v[i] == '  ' or type(v[i]) is list):
                par = [estados[i], k]
                transacoes = dict()
                for caracter in automato['alfabeto']:
                    transacoes[caracter] = [automato['transacoes'][par[0]][caracter],
                                            automato['transacoes'][par[1]][caracter]]

                marcou = False
                for key, parTransacao in transacoes.items():
                    if parTransacao[0] == parTransacao[1]:
                        continue

                    if marcou == True:
                        marcou = False
                        break

                    if buscarValorCelula(tabela, estados, parTransacao) == '  ':
                        setarValorCelula(tabela, estados, parTransacao, [par])
                    elif buscarValorCelula(tabela, estados, parTransacao) == ' x':
                        encabecado = buscarValorCelula(tabela, estados, par)
                        if type(encabecado) is list:
                            while len(encabecado) != 0:
                                for parEncab in encabecado:
                                    if buscarValorCelula(tabela, estados, parEncab) is list:
                                        encabecado.append(buscarValorCelula(
                                            tabela, estados, parEncab))
                                    setarValorCelula(
                                        tabela, estados, parEncab, ' x')
                                    encabecado.remove(parEncab)
                                    if len(encabecado) == 0:
                                        setarValorCelula(
                                            tabela, estados, par, ' x')
                                        marcou = True
                    else:
                        lista = buscarValorCelula(
                            tabela, estados, parTransacao)
                        if par not in lista:
                            lista.append(par)
    estados.pop()
    equivalentes = []
    for k, v in tabela.items():
        for index, value in enumerate(v):
            if type(value) is list or value == '  ':
                tabela[k][index] = "eq"
                par = [estados[index], k]
                equivalentes.append(par)

    print('Tabela:')
    pp.pprint(tabela)
    print(f'          {estados}')
    print('\nOs estados equivalentes são: ')
    for v in equivalentes:
        print(f'O estado {v[0]} é equivalente ao estado {v[1]}')


def buscarValorCelula(tabela, estados, par):
    indiceEstado1 = estados.index(par[0])
    indiceEstado2 = estados.index(par[1])
    tamanho = 0
    if par[0] in tabela:
        tamanho = len(tabela[par[0]])
    else:
        tamanho = len(tabela[par[1]])
    if tamanho >= indiceEstado2 + 1:
        return tabela[par[0]][indiceEstado2]
    else:
        return tabela[par[1]][indiceEstado1]


def setarValorCelula(tabela, estados, par, valor):
    indiceEstado1 = estados.index(par[0])
    indiceEstado2 = estados.index(par[1])
    tamanho = 0
    if par[0] in tabela:
        tamanho = len(tabela[par[0]])
    else:
        tamanho = len(tabela[par[1]])

    if tamanho >= indiceEstado2 + 1:
        if indiceEstado1 < tamanho:
            tabela[par[0]][indiceEstado1] = valor
    else:
        tabela[par[1]][indiceEstado1] = valor


instrucoes()
menu()
