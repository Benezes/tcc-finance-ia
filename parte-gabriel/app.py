# Instalando as dependencias
# Chamando um arquivo executavel para instalar os pip's
import subprocess
subprocess.call([r'pips.bat'])


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
import json


# Consumindo os dados da API Yahoo Finance
url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

# Passando a frequencia, o periodo e o nome da ação
periodo1 = "1577865600" # 01/01/2020
periodo2 = calendar.timegm(time.gmtime()) # Gerando um timestamp com a data de hoje
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

# Criando um dataframe pegando apenas o o objeto 'prices'
df = pd.DataFrame(dados["prices"])

# Transformando o df['date'] que era um índice que estava em formato Unix timestamp em datetime
df['date'] = pd.to_datetime(df['date'],unit='s')

# invertendo o df
df = df.iloc[::-1]

# Mostrando apenas o 5 primeros dias
#df.head(5)
df_data = df.iloc[:,0:5]
df_data

# Do DataFrame, o único dado que vamos usar é o close(fechamento)
df = df.iloc[:,[4]]

# Definimos um dia X que queremos prever. No nosso caso 21 dias pra frente
previsao_dias = 21

# Criando uma nova coluna 
df['prediction'] = df[['close']].shift(-previsao_dias)

 # data frame que vamos usar para fazer a previsão
df

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
print("Confiança SVM .: ", svm_confianca)

lr_confianca = lr.score(X_test, Y_test)
print("Confiança Regreção Linear.: ", lr_confianca)

tree_confianca = tree.score(X_test, Y_test)
print("Confiança Árvore de decisção .: " , tree_confianca)

# Puxando apenas os valores a serem previstos
previsto = np.array(df.drop(['prediction'],1))[-previsao_dias:]
previsto

svm_predict = svm.predict(previsto)
lr_predict = lr.predict(previsto)
tree_predict = tree.predict(previsto)

print("Previsão do SVM: ", svm_predict)
print("|\n|")
print("Previsão da regresão linear: ", lr_predict)
print("|\n|")
print("Previsão da árvore: ", tree_predict)

# Média da SVM
soma = 0
for i in svm_predict:
    soma += i

media = soma / svm_predict.size
print("Média do SVM: ", media)

# Média da regressão linear
soma = 0
for i in lr_predict:
    soma += i

media = soma / lr_predict.size
print("Média da regressão linear: ", media)

# Média da tree predict 
# Quanto tempo demora pra calcular essa média
soma = 0
for i in tree_predict:
    soma += i

media = soma / tree_predict.size
print("Média da arvore de decisção: ", media)
