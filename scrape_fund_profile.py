from bs4 import BeautifulSoup
import requests, json
from datetime import datetime as dt

dot_replace = lambda x: int(x.replace(".", ""))
convert_time = lambda x: dt.strptime(x, "%H:%M")
lambda_str = lambda x: str(x) if x != " " else None
lambda_int = lambda x: dot_replace(x) if x != " " else None
lambda_time = lambda x: convert_time(x) if x != " " else None

mapping = {
    'Kodu': str,
    'TEFAS İşlem Başlangıç Saati': lambda_str,
    #lambda x:dt.strptime(x, "%H:%M"),
    'Fon Alış Valörü': lambda_int,
    'TEFAS Min. Alış İşlem Miktarı ': lambda_int,
    'TEFAS Max. Alış İşlem Miktarı ': lambda_int, 
    'TEFAS İşlem Durumu': lambda_str,
    'Çıkış Komisyonu': lambda_str, 
    'ISIN Kodu': lambda_str,
    'TEFAS Son İşlem Saati': lambda_str,
    # lambda x:dt.strptime(x, "%H:%M"),
    'Fon Satış Valörü': lambda_int,
    'TEFAS Min. Satış İşlem Miktarı ': lambda_int,
    'TEFAS Max. Satış İşlem Miktarı ': lambda_int,
    'Giriş Komisyonu': lambda_str
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
        try:
            profile[headers[i]] = mapping[headers[i]](values[i])
            #profile[headers[i]] = values[i]
        except Exception:
            profile[headers[i]] = None
    return profile


with open("/Users/arman/Desktop/Git/Web_Scraping/funds.json", "r") as fp:
    fund_codes = list(map(lambda x: x["FONKODU"], json.load(fp)["data"]))


fund_profile_dict = {}
for f in fund_codes:
    r = getFundProfile(f)
    if r['TEFAS İşlem Durumu'] != 'İşlem Görmüyor':
        fund_profile_dict[f] = r

with open("fund_profiles.json", "w", encoding='utf8') as fp:
    json.dump(fund_profile_dict, fp, ensure_ascii=False)