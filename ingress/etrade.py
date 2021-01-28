import pandas as pd
from util import ingressutil

class ETradeIngress:

  @staticmethod
  def is_valid(data_to_check: pd.DataFrame) -> bool:

    first_col_name = data_to_check.columns[0]
    return ('Account Summary' == first_col_name)


  @staticmethod
  def transform_data(statement: pd.DataFrame) -> []:
    
    # Find the first row that is the actual header row
    # Find the last row that ends the data table
    # Get the rows between header row and end row
    # Create a new table with new headers from the header row

    datatable = ingressutil.read_data_table(statement,
        lambda df: (df.iloc[:,0] == 'Symbol') & (df.iloc[:,1] == 'Last Price $'),
        lambda df: (df.iloc[:,0] == 'TOTAL') & (df.iloc[:,1].isna())
    )

    # print('ETrade datatable: ', datatable)

    poss = []

    for index, row in datatable.iterrows():
      index # useless statement to get rid of pylint warnning
      if row['Last Price $'] == '--':
          # This is the lot row
          poss.append([symbol, 'ETrade', row['Symbol'].strip(), float(row['Quantity']), lastprice])
      else:
          # This is the symbol row
          symbol = row['Symbol']
          lastprice = float(row['Last Price $'])

    return poss

# sttmnt = pd.read_csv('../data/PortfolioDownload.csv',  thousands=',')

# print("is_valid: ", ETradeIngress.is_valid(sttmnt))
# print(ETradeIngress.transform_data(sttmnt))