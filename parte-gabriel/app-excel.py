import pandas as pd

df = pd.read_json (r'C:\Users\Gabriel Menezes\code-workspace\python\entendendo-api\krl.json')

df.to_csv(r'C:\Users\Gabriel Menezes\code-workspace\python\entendendo-api\dantas.csv', index = None)