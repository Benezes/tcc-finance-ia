 
# Instalando as dependências
'''
%pip install requests
%pip install pandas
%pip install numpy
%pip install install Quandl
%pip install scikit-learn
'''
 
# Importando as bibliotecas
import requests
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split 
import calendar
import time
 



# Consumindo os dados da API Yahoo Finance
url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"
 
# Passando a frequencia, o período e o nome da ação
periodo1 = "1577841776" # 01/01/2020
periodo2 = calendar.timegm(time.gmtime()) # Timestamp de hoje
acao = "AMZN"
 
querystring = {"frequency": "1d", "filter": "history",
               "period1": periodo1, "period2": periodo2, "symbol": acao}
 
key = "5ff9fb4e8fmsh9d016c18191002fp1d1248jsn149d5adf2e0e"
headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': key
}
 
response = requests.request("GET", url, headers=headers, params=querystring)
 
# Passando o retorno para uma variavel que transformara o retorno em um JSON
dados = response.json()
 
# Criando um dataframe pegando apenas o objeto 'prices'
df = pd.DataFrame(dados["prices"])
 
# Transformando o df['date'] que era um índice que estava em formato Unix timestamp em datetime
df['date'] = pd.to_datetime(df['date'],unit='s')
 
# invertendo o df
df = df.iloc[::-1]
 
# Data frame da data, open, high, low e close
df_data = df.iloc[:,0:5]
# Do DataFrame, o único dado que vamos usar é o close(fechamento)
# data frame que vamos usar para fazer a previsão
df = df.iloc[:,[4]]
 
# Definimos um dia X que queremos prever. No nosso caso 21 dias pra frente
previsao_dias = 21
 
# Criando uma nova coluna 
df['prediction'] = df[['close']].shift(-previsao_dias)
 
'''
Imagine pegar os primeiros 21 dias de fechamento do mercado para fazer o algoritmo
prever 21 dias pra frente
'''


# Pegando todo o valor do fechamento menos os que vamos prever que definimos como 21 dias
# *Criando um data set independente chamado X*
# Tirando a coluna prediction do data set e transformando ele em um np_array
X = np.array(df.drop(['prediction'],1))
 
# pegando todas os valores de Y menos as 21 últimas linhas
X = X[:-previsao_dias]




# *Criando um data set independente chamado X*
# Tirando a coluna prediction do df e transformando ele em um np_array
Y = np.array(df['prediction'])
 
# pegando todas os valores de Y menos as 21 primeiras linhas
Y = Y[:-previsao_dias]


# Dividindo os valores dos dados
# 80% dos dados é para treinamento
# 20% dos dados é para teste
 
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)


# Criando alguns modelos de treinamentos com alguns algoritmos
# Modelo de treinamento com SVM
svm = SVR(kernel='rbf', C=1e3, gamma=0.1)
svm.fit(X_train, Y_train)
 
# Modelo de treinamento com Árvore de decisão regressiva
tree = DecisionTreeRegressor().fit(X_train, Y_train)
 
# Modelo de treinamento com Regressão Linear
lr = LinearRegression().fit(X_train, Y_train)


'''
Criando o Modelo de teste!: 
A pontuação retorna o coeficiente de determinação R^2 da predição
A melhor possibilidade de score/pontuação é 1.0
Ou seja, quanto maior a pontuação melhor a confiança do algoritmo
'''
svm_confianca = svm.score(X_test, Y_test)
 
lr_confianca = lr.score(X_test, Y_test)
 
tree_confianca = tree.score(X_test, Y_test)


# Puxando apenas os valores a serem previstos
previsto = np.array(df.drop(['prediction'],1))[-previsao_dias:]



# Lista de previsão dos algoritmos
svm_predict = svm.predict(previsto)
lr_predict = lr.predict(previsto)
tree_predict = tree.predict(previsto)


# Lista que receberá a médias das previsões
predicts_score = []


# Média da SVM
soma = 0
for i in svm_predict:
    soma += i
 
media_svm = soma / svm_predict.size
predicts_score.append(media_svm)


# Média da regressão linear
soma = 0
for i in lr_predict:
    soma += i
 
media_lr = soma / lr_predict.size
predicts_score.append(media_lr)


# Média da tree predict 
# Quanto tempo demora pra calcular essa média
soma = 0
for i in tree_predict:
    soma += i
 
media_tree = soma / tree_predict.size
predicts_score.append(media_tree)


'''
Todas as médias que foram inseridas na lista de predicts
agora sera ordenada de maneira reversa para assim 
pegarmos apenas o primeiro valor que é o score com melhor média.
Em seguida pego o último fechamento da ação 
para fazer uma comparação com a média.
'''
predicts_score.sort(reverse = True)
 
melhorMediaPredict = int(predicts_score[0])
 
primeiraData = df_data.tail(1)
fechamentoDaPrimeiraData = primeiraData["close"]
fechamento = int(fechamentoDaPrimeiraData)


'''
0 = Se o fechamento estiver acima da média de 21 períodos = TENDÊNCIA DE ALTA
1 = Se o fechamento estiver abaixo da média de 21 períodos = TENDÊNCIA DE BAIXA
'''
def mediaFechamento(fehamento, media):
    if fehamento > media:
        return 0
    elif fechamento < media:
        return 1
 
mediaFechamento(fechamento, melhorMediaPredict)
