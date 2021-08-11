import json
import pandas as pd

fd = open('Web_Scraping/Executions/execution.json', 'r')
json_file = json.load(fd)

lookup_table = pd.read_csv('Web_Scraping/Executions/fund_profiles.csv')
df = pd.DataFrame(data=lookup_table)

for customer_exec in json_file[:5]:
    amount = customer_exec['amount']
    source = customer_exec['source']
    destination = customer_exec['destination']
    source_df = df.query('Kodu in @source')
    destination_df = df.query('Kodu in @destination')

    amount_portfolio = {}
    source_keys = source.keys()
    for key in source_keys:
        amount_portfolio[key] = source[key] * amount
    
    print(amount_portfolio)


