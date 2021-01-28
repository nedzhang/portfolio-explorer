import os
from glob import glob
import pandas as pd
import requests
from bs4 import BeautifulSoup

from ingress.etrade import ETradeIngress
from ingress.fidelity import FidelityIngress
from ingress.morgan import MorganStockPlanIngress
from ingress.vanguard import VanguardIngress


STOCK_PRICE_LOOKUP_URL_TEMPLATE = "https://finance.yahoo.com/quote/{}"

price_dictionary = {}

def getPrice(symbol: str) -> float:

  key = symbol.upper()

  if key in price_dictionary:
    return price_dictionary[key]
  else:
    queryurl = STOCK_PRICE_LOOKUP_URL_TEMPLATE.format(symbol.upper())

    quotepage = requests.get(queryurl)

    quotepage_soup= BeautifulSoup(quotepage.text, 'html.parser')
    # print(quotepage_soup)

    pricespan = quotepage_soup.select(r'span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)')

    if pricespan is not None and len(pricespan) == 1:
      pricetext = pricespan[0].text

      # print('pricetext: ', pricetext)
      price = float(pricetext.replace(',', ''))
      price_dictionary.update({key: price})
      return price
    else :
      price_dictionary.update({key: None})
      return None

def load_downloadfiles(folderpath:str) -> [pd.DataFrame]:
    
    downloadfiles = []

    for filename in glob(os.path.join(folderpath, '*.xls')):
        # print(filename)
        downloadfiles.append(pd.read_excel(filename, thousands=','))

    for filename in glob(os.path.join(folderpath, '*.csv')):
        # print(filename)
        downloadfiles.append(pd.read_csv(filename, thousands=','))

    return downloadfiles

def consolidate_downloads(downloads: [pd.DataFrame]) -> pd.DataFrame:
    positions = []

    for dl in downloads:

        if ETradeIngress.is_valid(dl):
            positions += ETradeIngress.transform_data(dl)
        elif FidelityIngress.is_valid(dl):
            positions += FidelityIngress.transform_data(dl)
        elif MorganStockPlanIngress.is_valid(dl):
            positions += MorganStockPlanIngress.transform_data(dl)
        elif VanguardIngress.is_valid(dl):
            positions += VanguardIngress.transform_data(dl)


    position_table = pd.DataFrame(data=positions, 
    columns=['symbol', 'institute', 'account', 'shares', 'price'])

    position_table = position_table.sort_values(by=['symbol', 'institute', 'account'])

    return position_table

def update_price(positions: pd.DataFrame) -> pd.DataFrame:
  
    for index, row in positions.iterrows():
        symbol = row['symbol']
        print('get price for: ', symbol)

        price = getPrice(symbol)

        if (price is not None):
          positions.at[index, 'price'] = price

    # totals = []
    # for index, row in positions.iterrows():
    #     totals.append(row['shares'] * row['price'])

    positions['total'] = positions['shares'] * positions['price']

    return positions

GET_HOLDING_URL_TEMPLATE = 'https://finance.yahoo.com/quote/{}/holdings?{}'

def get_holding(symbol: str) -> pd.DataFrame:

    try:
        url = GET_HOLDING_URL_TEMPLATE.format(symbol, symbol)
        print("url: ", url)
        tables = pd.read_html(url)
    except ValueError:
        print('cannot get quote for {}. Use it as is'.format(symbol))
        # Can't get anything for the symbol. Probably one of those target date fund
        return None
    else:
        if tables is None or len(tables) != 1:
            # More than 1 table. Probably is stock not MF
            return None
        else:
            # Only 1 table. Should be the holdings of MF
            return tables[0]


def explore_portfolio_holdings(positions: pd.DataFrame) -> pd.DataFrame:

    # Break out the holdings in MFs and ETF
    holdings = []

    for index, row in positions.iterrows() :
        index
        symbol = row["symbol"]
        total = row['total']
        symbol_holding = get_holding(symbol)
        
        if symbol_holding is None:
            # No holding information, just copy the row over
            entry = [
                symbol, row['institute'], row['account'], symbol, '100', row['shares'], row['price'], row['total']
            ]
            holdings.append(entry)
        else:
            percent_accounted = 0.0

            for holdingindex, holdingrow in symbol_holding.iterrows():
                holdingindex
                holdingsymbol = holdingrow['Symbol']
                if holdingsymbol is None or pd.isna(holdingsymbol):
                    holdingsymbol = holdingrow['Name'] 
                holdingpercent = float(holdingrow['% Assets'].replace('%', ''))
                percent_accounted += holdingpercent
                holdingvalue = total * holdingpercent / 100.0
                entry = [holdingsymbol, row['institute'], row['account'], symbol, holdingpercent, None, None, holdingvalue]
                holdings.append(entry)
            
            percent_left = 100 - percent_accounted

            holdings.append([symbol + '-UNKNOWN', row['institute'], row['account'], symbol, percent_left, None, None, total * percent_left/100.0])
            
    detail_table =  pd.DataFrame(data=holdings, columns=['symbol', 'institute', 'account', 'source', 'percentage', 'shares', 'price', 'total'])

    return detail_table