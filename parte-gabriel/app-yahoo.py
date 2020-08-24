import requests

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"

# Parametros
querystring = {"frequency":"1d",
               "filter":"history",
               
               # REQUIRED Epoch timestamp in seconds 
               "period1":"915192000",
               
               # REQUIRED Epoch timestamp in seconds 
               "period2":"1562086800",
               "symbol":"AMRN"
               }

# Autenticação 
headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "5ff9fb4e8fmsh9d016c18191002fp1d1248jsn149d5adf2e0e"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)