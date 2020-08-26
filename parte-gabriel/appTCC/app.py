# Chamando a API
import requests
import pandas as pd
import json
import numpy as np
from datetime import datetime


url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

querystring = {"frequency": "1d", "filter": "history",
               "period1": "1546448400", "period2": "1562086800", "symbol": "AMRN"}

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "5ff9fb4e8fmsh9d016c18191002fp1d1248jsn149d5adf2e0e"
}

response = requests.request("GET", url, headers=headers, params=querystring)

# Forma nutela de inserir o json no Excel
dados = response.json()
df = pd.DataFrame(dados["prices"])

# print(df.to_json(orient='split'))
df.to_csv(r'yah-finance.csv', index=None)

ds = pd.read_csv('yah-finance.csv')

columnDate = ds.iloc[:, :1].values
columnOpen = ds.iloc[:, 1:2].values
columnClose = ds.iloc[:, 4:5].values

def converteData():
    '''
        Função que converte um Epoch & Unix Timestamp para datetime.
        Como eu recebo uma lista de datas com o formato timestamp 
        retorno uma lista no formato datetime.
    '''
    lst = []
    for data in columnDate:
        datas = datetime.fromtimestamp(data)
        lst.append(str(datas))
    return lst

colunaData = np.asarray(converteData())
print(colunaData)
print(columnDate)

