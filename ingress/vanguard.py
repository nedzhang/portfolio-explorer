import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from util import ingressutil


VANGUARD_SYMBOL_LOOKUP_URL_TEMPLATE = 'https://investor.vanguard.com/search/?query={}'
vangaurd_symbol_cache = {}

class VanguardIngress:

  @staticmethod
  def getVanguardSymbol(fundname: str) -> str:
    
    if fundname in vangaurd_symbol_cache:
      return vangaurd_symbol_cache[fundname]
    else:
      queryurl = VANGUARD_SYMBOL_LOOKUP_URL_TEMPLATE.format(requests.utils.quote(fundname))

      fundlistpage = requests.get(queryurl)

      fundlistpage_soup= BeautifulSoup(fundlistpage.text, 'html.parser')

      links = fundlistpage_soup.select('a.twitter-button')

      if links is not None and len(links) > 0:
        url = links[0]['url']
        # print (url)
        tokens = os.path.split(url)
        if tokens is not None and len(tokens) == 2:
          symbol = tokens[1]
          vangaurd_symbol_cache.update({fundname: symbol})
          return symbol

      print('Cannot find symbol for "{}". Url: {}'.format(fundname, queryurl))
      return "UNKOWN ({})".format(fundname)

  @staticmethod
  def is_valid(data_to_check: pd.DataFrame) -> bool:

    first_col_name = data_to_check.columns[0]
    return ('Fund Account Number' == first_col_name)


  @staticmethod
  def transform_data(statement: pd.DataFrame) -> []:
    
    # Find the first row that is the actual header row
    # Find the last row that ends the data table
    # Get the rows between header row and end row
    # Create a new table with new headers from the header row

    datatable = ingressutil.read_data_table(statement, None, None)

    # print('Vanguard datatable: ', datatable)

    poss = []
    
    ass = datatable[pd.to_numeric(datatable['Shares'], errors='coerce')> 0]
    # print(ass)

    for index, row in ass.iterrows():
      index,
      fundname = row['Fund Name']
      symbol = VanguardIngress.getVanguardSymbol(fundname)
      poss.append([symbol, 'Vanguard', row['Fund Account Number'].strip(), float(row['Shares']), float(row['Price'])])

    return poss


# sttmnt = pd.read_csv('../data/Copy of ofxdownload-1.csv',  thousands=',')

# print("is_valid: ", VanguardIngress.is_valid(sttmnt))
# print(VanguardIngress.transform_data(sttmnt))