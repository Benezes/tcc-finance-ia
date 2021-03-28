'''
imports
'''
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
Carregamento da base de dados
'''

# Importando a base de treinamento
base = pd.read_csv('petr4_treinamento.csv')

# Exlcuindo alguns valores nulos
base = base.dropna()

# Buscando os valores de fechamento do mercado
base_treinamento = base.iloc[:, 4:5].values
#print(base)

# Aplicando uma normalização para colocar esses valores numa escala de 0 até 1
normalizador = MinMaxScaler(feature_range=(0,1))

# Normalizando uma base de treinamento. Range de 0 até 1
base_treinamento_normalizada = normalizador.fit_transform(base_treinamento)

'''
pré processamento da base de dados
'''

# Para saber quando que a ação ira valer hoje irei pegar 90 dias pra trás
previsores = [] # aqui fica os 90 dias anteriores
preco_real = []

# quantos preços devo pegar, quantidade de registros
for i in range(90, 1242):
    previsores.append(base_treinamento_normalizada[i-90:i, 0])# Adicionando os 90 registros anteriores em previsores[]
    preco_real.append(base_treinamento_normalizada[i, 0])

previsores, preco_real = np.array(previsores), np.array(preco_real) # Transformando a lista de previsores e preco real em numpy array
previsores = np.reshape(previsores, (previsores.shape[0], previsores.shape[1], 1)) # Fazendo um redimencionamento na lista de previsores

'''
construção da rede neural, LSTM, que tem  5 camadas
'''

es = EarlyStopping(monitor = 'loss', min_delta = 1e-10, patience = 10, verbose = 1) # Se passar 10 épocas sem melhorar o treinamento para de treinar
rlr = ReduceLROnPlateau(monitor = 'loss', factor = 0.2, patience = 5, verbose = 1) # Reduz a métrica de aprendizagem quando para de melhorar
mcp = ModelCheckpoint(filepath = 'pesos.h5', monitor = 'loss', save_best_only = True, verbose = 1) # Sempre salva o melhor modelo

regressor = Sequential()

# unit é neuronio
# as camadas é oq fica entre a entrada e saida

# Primeira camada
regressor.add(LSTM(units = 200, return_sequences = True, input_shape = (previsores.shape[1], 1))) # Quanto mais units mais neuronio de memorias.
regressor.add(Dropout(0.3))

# Segunda camada
regressor.add(LSTM(units = 150, return_sequences = True))
regressor.add(Dropout(0.3))

# Terceira camada
regressor.add(LSTM(units = 150, return_sequences = True))
regressor.add(Dropout(0.3))

# Quarta camada
regressor.add(LSTM(units = 150, return_sequences = True))
regressor.add(Dropout(0.3))

# Quinta camada
regressor.add(LSTM(units = 150, return_sequences = True))
regressor.add(Dropout(0.3))

# Camada densa
# é na camada densa que vamos achar  a solução da equação diferencial com o sigmoid
regressor.add(Dense(units = 1, activation = 'sigmoid'))

regressor.compile(optimizer = 'rmsprop', loss = 'mean_squared_error', metrics = ['mean_absolute_error'])

# método fit irá treinar o modelo
regressor.fit(previsores, preco_real, epochs = 100, batch_size = 32, callbacks = [es, rlr, mcp])



'''
Previsão dos preços das ações
preco_real_teste sera oque irei usar para comparar oque a previsão fez
'''
base_teste = pd.read_csv('petr4_teste.csv')
preco_real_teste = base_teste.iloc[:, 4:5].values # Queremos apenas o close

base_completa = pd.concat((base['Close'], base_teste['Close']), axis = 0)  # Fazendo a extração dos 90 preços anteriores

entradas = base_completa[len(base_completa) - len(base_teste) - 90:].values
entradas = entradas.reshape(-1, 1)
entradas = normalizador.transform(entradas)

X_teste = []
for i in range(90, 112):
    X_teste.append(entradas[i - 90:i, 0])

X_teste = np.array(X_teste)
X_teste = np.reshape(X_teste, (X_teste.shape[0], X_teste.shape[1], 1))

# Previsões 
previsoes = regressor.predict(X_teste)
previsoes = normalizador.inverse_transform(previsoes) # Desnormalizando
qtd_previsoes = previsoes.size


'''
Comparações
'''
print('Previsoes')
print(previsoes)
print('\nPreço real')
print(preco_real_teste)
print("\n\n****************\n")
print('Média entre a previsão e o preço real')
print(f'Média das previsoes: {previsoes.mean()}')
print(f'Média dos preços reais: {preco_real_teste.mean()}')
print(f'Diferença de: {preco_real_teste.mean() - previsoes.mean()}')


 '''
Gráfico 
'''
plt.figure(figsize=(30,10))
plt.plot(preco_real_teste, color = 'red', label = 'Preço real')
plt.plot(previsoes, color = 'blue', label = 'Previsões')
plt.title('Previsão preços das ações')
plt.xlabel("Tempo")
plt.ylabel("Valor")
plt.legend()
plt.show()
