import requests
import json
import pandas as pd
import csv

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

# Buscando as ações diarias da petrobras referente ao periodo: 01/01/2019 até 31/12/2019
# data convert to Epoch & Unix Timestamp
querystring = {"frequency": "1d", "filter": "history",
               "period1": "1546344000", "period2": "1577793600", "symbol": "PETR4.SA"}

# Passando os paremetros do get em 'headers'
# Essa chave esta vinculada ao meu id
headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "5ff9fb4e8fmsh9d016c18191002fp1d1248jsn149d5adf2e0e"
}

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

# Gerando o json
# with open('financeData.json', 'w', encoding='utf-8') as f:
#     json.dump(response.json(), f, ensure_ascii=False, indent=4)


# Transformando o json em arquivo .csv
data = json.loads(response.text)

for i in data["prices"]:
    print(i["date"] + ';' + i["open"])
