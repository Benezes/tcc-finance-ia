# Chamando a API
import requests

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

querystring = {"frequency":"1d","filter":"history","period1":"1546448400","period2":"1562086800","symbol":"AMRN"}

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "5ff9fb4e8fmsh9d016c18191002fp1d1248jsn149d5adf2e0e"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

# Forma nutela
import pandas as pd
import json 

dados = response.json()
df = pd.DataFrame(dados["prices"])

#print(df.to_json(orient='split'))
df.to_csv(r'teste.csv', index = None)
