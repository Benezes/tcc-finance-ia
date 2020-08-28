#Instale as dependencias
'''
%pip install requests
%pip install pandas
%pip install numpy
%pip install scikit-learn
'''


import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split 


url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

querystring = {"frequency": "1d", "filter": "history",
               "period1": "1596322800", "period2": "1598569200", "symbol": "AMZN"}

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "5ff9fb4e8fmsh9d016c18191002fp1d1248jsn149d5adf2e0e"
}

response = requests.request("GET", url, headers=headers, params=querystring)

dados = response.json()

df = pd.DataFrame(dados["prices"])
#print(dados)
#print(df)

columnDate = pd.to_datetime(df['date'],unit='s')
columnOpen = df['open']
columnHigh = df['high']
columnLow = df['low']
columnClose = df['close']
columnVolume = df['volume']


# Transformando o df['date'] que era um índice que estava em formato Unix timestamp em datetime
df['date'] = pd.to_datetime(df['date'],unit='s')

# Pritando o date, open, high, low e close
print(df.iloc[:,:5])

df = df.iloc[:,[4]] 

print(df)

# (N) dias de previsão
previsao_dias = 1 

#df_previsao = date_close

# Criando uma nova coluna 
df['prediction'] = df[['close']].shift(-previsao_dias)# data frame que vamos usar para fazer a previsão

# *Criando um data set independente chamado X*
# Tirando a coluna prediction do df e transformando o df_previsao em um np_array
X = np.array(df.drop(['prediction'],1))

# Removendo as ultimas 30 linhas de close, pois vamos prever o valor do close delas
X = X[:-previsao_dias]
print(X)

# *Criando um data set independente chamado X*
# Tirando a coluna prediction do df e transformando o df_previsao em um np_array

Y = np.array(df['prediction'])

# pegando todas os valores de Y menos as 30 últimas linhas
Y = Y[:-previsao_dias]
print(Y)

# Dividindo os valores dos dados
# 80% dos dados é para treinamento
# 20% dos dados é para teste

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)

# # Vou usar dois tipos de algoritmo/modelo de previsão, SVM (Support Vector Machine (regressor)) e Regressão Linear #

# Criando e Treinando! os modelos usando o SVM
svm_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svm_rbf.fit(X_train, Y_train,)

#Criando o Modelo de teste!: 
#A pontuação retorna o coeficiente de determinação R^2 da predição
# A melhor possibilidade de score/pontuação é 1.0

# !Quanto menor o score/pontuação menor a confiança!
svm_confianca = svm_rbf.score(X_test, Y_test)
print("SVM Confiança.: ", svm_confianca)

# Criando e Treinando! o modelo de regressão linear
rl = LinearRegression()
rl.fit(X_train, Y_train)

#A pontuação retorna o coeficiente de determinação R^2 da predição
# A melhor possibilidade de score/pontuação é 1.0

rl_confianca = rl.score(X_test, Y_test)
print("Regreção Linear Confiança.: ", rl_confianca)

# Quanto maior o score de confiança dos algoritmos melhor pra prever o valor de fechamento

# pegando o dataframe, tirando a coluna prediction e tirando os dias de previsao
jesus = np.array(df.drop(['prediction'],1))[-previsao_dias:]
print(jesus)

# Momento da verdade

regressaoLinear = rl.predict(jesus)
print("Previsão da regressão linear")
print(regressaoLinear)

print("Previsão da SVM")
svm_predicao = svm_rbf.predict(jesus)
print(svm_predicao)

