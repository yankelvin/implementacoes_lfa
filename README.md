# implementacoes_lfa
Implementações de algoritmos da disciplina de Linguagens Formais e Autômatos

### Instruções:
* Para executar os algoritmos primeiro é necessário informar os dados do automato desejado.
    Dados necessários: alfabeto, estado inicial, estado final e transações. Seguir o modelo mostrado abaixo:
    
    ~~~json
    automato_teste1 = {
    "alfabeto": ["a", "b"],
    "estInicial": "q0",
    "estFinal": ["q2"],
    "transacoes": {
        "q0": {"a": "q1", "b": "q3"},
        "q1": {"a": "q3", "b": "q2"},
        "q2": {"a": "q2", "b": "q2"},
        "q3": {"a": "q3", "b": "q3"}
      }
    }
    ~~~
* No código há uma função de MENU com as seguintes opções:
    1 - Verificar se palavra é aceita pelo autômato
    2 - Minimizar o autômato e mostrar estados equivalentes
    
    Em cada uma delas há uma função que recebe como parâmetro o autômato desejado para executar as funções, após mapear o autômato no formato mostrado anteriormente, basta alterar o parâmetro que é recebido por cada função.
