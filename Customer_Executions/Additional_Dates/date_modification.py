import json, os
import pandas as pd
from datetime import datetime as dt, timedelta

folderpath = os.path.dirname(os.path.abspath(__file__))
fd = open(folderpath + '/execution.json', 'r')
json_file = json.load(fd)

lookup_table = pd.read_csv(folderpath + '/fund_profiles.csv')
df = pd.DataFrame(data=lookup_table)

def isValidDate(key, start_date):
    price_table = pd.read_csv(f"{folderpath}/Fund_Date_Data/{key}.csv")
    price_df = pd.DataFrame(data=price_table)

    check_df = price_df.query('data_date == @start_date')
    if check_df.empty:
        return False
    return True

def findValidDate(key, price_df, start_date):
    check_df = price_df.query('data_date == @start_date')
    while check_df.empty:
        dt_curr_date = dt.strptime(start_date, "%Y-%m-%d")
        curr_date = dt_curr_date.strftime("%Y-%m-%d")

        dt_next_date = dt_curr_date + timedelta(days=1)
        next_date = dt_next_date.strftime("%Y-%m-%d")
        check_df = price_df.query('data_date == @next_date')

        print(f"No price is found for {key} on date {curr_date}, trying {next_date}")
    return check_df

def getFundPrice(key, start_date):
    price_table = pd.read_csv(f"{folderpath}/Fund_Date_Data/{key}.csv")
    price_df = pd.DataFrame(data=price_table)
    price_df = findValidDate(key, price_df, start_date)
    return price_df['price'].values[0]

def getFundData(fund_type, amount, start_date, valor_tipi, fund_portfolio_dict, fund_valor_dict):
    fund_keys = fund_type.keys()
    fund_type_df = df.query('Kodu in @fund_type')
    for key in fund_keys:
        fund_df = fund_type_df.query('Kodu == @key')
        valor = fund_df[valor_tipi].values[0]
        
        fund_price= getFundPrice(key, start_date)

        fund_portfolio_dict[key] = (fund_type[key] * amount) // fund_price
        fund_valor_dict[key] = valor

def dayPasses(queue):
    # Each arr popped from queue has the following format
    # arr = [key, valor, curr_date]
    temp_queue = []
    while len(queue) != 0:
        arr = queue.pop()
        if arr[1] != 0:
            arr[1] -= 1
        arr[2] = arr[2] + timedelta(days=1)
        temp_queue.append(arr)
    return temp_queue

def findFundtoBuy(balance, fund_dest_portfolio, buy_date):
    for key in fund_dest_portfolio.keys():
        min_alis_miktari = ((df.query('Kodu in @destination')).query('Kodu == @key'))['TEFAS Min. Alış İşlem Miktarı '].values[0]

        price_table = pd.read_csv(f"{folderpath}/Fund_Date_Data/{key}.csv")
        price_df = pd.DataFrame(data=price_table)
        check_df = price_df.query('data_date == @buy_date')
        dt_buy_date = dt.strptime(buy_date, "%Y-%m-%d")
        
        if not (check_df.empty):
            fund_price = check_df['price'].values[0]
            bought_shares = balance // fund_price
            
            if bought_shares >= min_alis_miktari:
                return [key, bought_shares, dt_buy_date, fund_price]
    return [' ', 0, dt_buy_date, 0]

for customer_exec in json_file[2:3]:  
    amount = customer_exec['amount']
    source = customer_exec['source']
    destination = customer_exec['destination']
    start_date = customer_exec['date']

    #Look for later
    destination_portfolio = {}

    fund_stock_portfolio = {}
    fund_stock_satis_valor = {}
    getFundData(source, amount, start_date, 'Fon Satış Valörü', fund_stock_portfolio, fund_stock_satis_valor)

    fund_dest_portfolio = {}
    fund_dest_alis_valor = {}
    getFundData(destination, amount, start_date, 'Fon Alış Valörü', fund_dest_portfolio, fund_dest_alis_valor)

    #Model where we order all stocks in the portfolio to be sold immediately
    satim_queue = []
    alim_queue = []
    curr_date = start_date
    balance = 0

    for key in fund_stock_satis_valor.keys():
        dt_start_time = dt.strptime(start_date, "%Y-%m-%d")
        satim_queue.insert(0, [key, fund_stock_satis_valor[key], dt_start_time])
        print(f"Sell Order: Sold {key} with {fund_stock_portfolio[key]} shares on {start_date}.")
    
    while len(satim_queue) != 0 or len(alim_queue) != 0:
        #Sell subroutine
        len_satim_queue = len(satim_queue)
        for i in range(len_satim_queue):
            arr = satim_queue.pop()
            if arr[1] == 0 and isValidDate(arr[0], curr_date):
                balance += (getFundPrice(arr[0], curr_date) * fund_stock_portfolio[arr[0]])

            elif not (isValidDate(arr[0], curr_date)) and arr[1] == 0:
                print(f"No price is found for {arr[0]} on date {curr_date}")
                satim_queue.insert(0, arr)

            else:
                print(f"Pending Orders: {arr[1]} days left for selling {arr[0]} to be completed.")
                satim_queue.insert(0, arr)
        
        satim_queue = dayPasses(satim_queue)

        
        #Buy subroutine
        if balance != 0:
            key_arr = findFundtoBuy(balance, fund_dest_portfolio, curr_date)
            
            while key_arr[0] != ' ':
                # [key, key_valor, buy_date, bought_shares, fund_price]
                alim_queue.insert(0, [key_arr[0], fund_dest_alis_valor[key_arr[0]], key_arr[2], key_arr[1], key_arr[3]])
                print(f"Buy Order: Bought {key_arr[0]} with {key_arr[1]} shares.")

                # key_arr[1] = bought_shares , key_arr[3] = fund_price
                balance -= (key_arr[1] * key_arr[3])
                key_arr = findFundtoBuy(balance, fund_dest_portfolio, curr_date)
        
            print(f"You have ${balance} money in your brokerage account.")

        if len(alim_queue) != 0:
            len_alim_queue = len(alim_queue)
            
            for i in range(len_alim_queue):
                arr = alim_queue.pop()
                if arr[0] not in destination_portfolio.keys():
                    destination_portfolio[arr[0]] = 0
                if arr[1] == 0:
                    destination_portfolio[arr[0]] += arr[3]
                    print(f"Transaction for {arr[0]} is complete, you have {destination_portfolio[arr[0]]} shares.")
                else:
                    print(f"Pending Order: {arr[1]} days left for buying {arr[0]} to be completed.")
                    alim_queue.insert(0, arr)
            
            alim_queue = dayPasses(alim_queue)
            #What we have in our destination portfolio
            print(f"Your aimed portfolio is now {destination_portfolio}")
    
        #Update the day
        dt_curr_date = dt.strptime(curr_date, "%Y-%m-%d")
        dt_next_date = dt_curr_date + timedelta(days=1)
        curr_date = dt_next_date.strftime("%Y-%m-%d")
