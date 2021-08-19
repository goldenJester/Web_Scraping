import json, os
import pandas as pd

folderpath = os.path.dirname(os.path.abspath(__file__))
fd = open(folderpath + '/execution.json', 'r')
json_file = json.load(fd)

lookup_table = pd.read_csv(folderpath + '/fund_profiles.csv')
df = pd.DataFrame(data=lookup_table)

def getFundData(fund_type, amount, valor_tipi, fund_portfolio_dict, fund_valor_dict, fund_price_dict):
    fund_keys = fund_type.keys()
    fund_type_df = df.query('Kodu in @fund_type') 
    for key in fund_keys:
        fund_df = fund_type_df.query('Kodu == @key')
        fund_price = fund_df['price'].values[0]
        valor = fund_df[valor_tipi].values[0]

        fund_portfolio_dict[key] = (fund_type[key] * amount) // fund_price
        fund_valor_dict[key] = valor
        fund_price_dict[key] = fund_price

def dayPasses(queue):
    temp_queue = []
    while len(queue) != 0:
        arr = queue.pop()
        arr[1] -= 1
        temp_queue.append(arr)
    return temp_queue

def findFundtoBuy(balance, fund_dest_portfolio, fund_dest_price):
    for key in fund_dest_portfolio.keys():
        min_alis_miktari = ((df.query('Kodu in @destination')).query('Kodu == @key'))['TEFAS Min. Alış İşlem Miktarı '].values[0]
        bought_shares = balance // fund_dest_price[key]
        if bought_shares >= min_alis_miktari:
            return [key, bought_shares]
    return [' ', 0]

for customer_exec in json_file:  
    amount = customer_exec['amount']
    source = customer_exec['source']
    destination = customer_exec['destination']

    #Look for later
    destination_portfolio = {}

    fund_stock_portfolio = {}
    fund_stock_satis_valor = {}
    fund_stock_price = {}
    getFundData(source, amount, 'Fon Satış Valörü', fund_stock_portfolio, fund_stock_satis_valor, fund_stock_price)

    fund_dest_portfolio = {}
    fund_dest_alis_valor = {}
    fund_dest_price = {}
    getFundData(destination, amount, 'Fon Alış Valörü', fund_dest_portfolio, fund_dest_alis_valor, fund_dest_price)

    #Model where we order all stocks in the portfolio to be sold immediately
    satim_queue = []
    alim_queue = []
    balance = 0
    for key in fund_stock_satis_valor.keys():
        satim_queue.insert(0, [key, fund_stock_satis_valor[key]])
        print(f"Sell Order: Sold {key} with {fund_stock_portfolio[key]} shares.")
    
    while len(satim_queue) != 0 or len(alim_queue) != 0:
        #Sell subroutine
        len_satim_queue = len(satim_queue)
        for i in range(len_satim_queue):
            arr = satim_queue.pop()
            if arr[1] == 0:
                balance += (fund_stock_price[arr[0]] * fund_stock_portfolio[arr[0]])
            else:
                print(f"Pending Orders: {arr[1]} days left for selling {arr[0]} to be completed.")
                satim_queue.insert(0, arr)
        
        satim_queue = dayPasses(satim_queue)

        
        #Buy subroutine
        if balance != 0:
            key_arr = findFundtoBuy(balance, fund_dest_portfolio, fund_dest_price)
        while key_arr[0] != ' ':
            alim_queue.insert(0, [key_arr[0], fund_dest_alis_valor[key_arr[0]], key_arr[1]])
            print(f"Buy Order: Bought {key_arr[0]} with {key_arr[1]} shares.")
            balance -= (key_arr[1] * fund_dest_price[key_arr[0]])
            key_arr = findFundtoBuy(balance, fund_dest_portfolio, fund_dest_price)
        
        print(f"You have ${balance} money in your brokerage account.")

        if len(alim_queue) != 0:

            len_alim_queue = len(alim_queue)
            for i in range(len_alim_queue):
                arr = alim_queue.pop()
                if arr[0] not in destination_portfolio.keys():
                    destination_portfolio[arr[0]] = 0
                if arr[1] == 0:
                    destination_portfolio[arr[0]] += arr[2]
                    print(f"Transaction for {arr[0]} is complete, you have {fund_dest_portfolio[arr[0]]} shares.")
                else:
                    print(f"Pending Order: {arr[1]} days left for buying {arr[0]} to be completed.")
                    alim_queue.insert(0, arr)
            
            alim_queue = dayPasses(alim_queue)
            #What we have in our destination portfolio
            print(f"Your aimed portfolio is now {destination_portfolio}")


    ## O gun verdigim emirler orderlar
    ## Pending orders
    ## O gunku balance
    ## Su an elimde ne var -- stock list




