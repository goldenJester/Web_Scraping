from bs4 import BeautifulSoup
import requests, json
from datetime import datetime as dt

mapping = {
    'Kodu': str,
    'TEFAS İşlem Başlangıç Saati': str,
    #lambda x:dt.strptime(x, "%H:%M"),
    'Fon Alış Valörü': str,
    'TEFAS Min. Alış İşlem Miktarı ': str,
    'TEFAS Max. Alış İşlem Miktarı ': str, 
    'TEFAS İşlem Durumu': str,
    'Çıkış Komisyonu': str, 
    'ISIN Kodu': str,
    'TEFAS Son İşlem Saati': str,
    #lambda x:dt.strptime(x, "%H:%M"),
    'Fon Satış Valörü': str,
    'TEFAS Min. Satış İşlem Miktarı ': str,
    'TEFAS Max. Satış İşlem Miktarı ': str,
    'Giriş Komisyonu': str
}

def getFundProfile(fund_code):
    html_text = requests.get(f'https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod={fund_code}').text


    soup = BeautifulSoup(html_text, 'lxml')
    fund_profile = soup.find('div', class_="fund-profile")
    fund_categories = fund_profile.find_all('tr', class_="fund-profile-row")
    fund_categories += fund_profile.find_all('tr', class_="fund-profile-alternate")

    ## the last category returned is a link with element <a></a>
    del fund_categories[-1]

    headers = []
    values = []
    for category in fund_categories:
        values += category.find('td', class_="fund-profile-item")
        headers += category.find('td', class_="fund-profile-header")

    profile = {}
    for i in range(len(headers)):
        # profile[headers[i]] = values[i]
        profile[headers[i]] = mapping[headers[i]](values[i])
    
    print(profile)
    return profile

with open("funds.json", "r") as fp:
    fund_codes = list(map(lambda x:x["FONKODU"], json.load(fp)["data"]))


fund_profile_dict = {}
for f in fund_codes[:5]:
    r = getFundProfile(f)
    fund_profile_dict[f] = r

with open("fund_profiles.json", "w", encoding='utf-8') as fp:
    json.dump(fund_profile_dict, fp)










