import pandas as pd
from util import ingressutil

class MorganStockPlanIngress:

  @staticmethod
  def is_valid(data_to_check: pd.DataFrame) -> bool:

    first_col_name = data_to_check.columns[0]

    return ('Unnamed: 0' == first_col_name)


  @staticmethod
  def transform_data(statement: pd.DataFrame) -> []:
    
    # Find the first row that is the actual header row
    # Find the last row that ends the data table
    # Get the rows between header row and end row
    # Create a new table with new headers from the header row

    datatable = ingressutil.read_data_table(statement,
        lambda df: (df['Unnamed: 0'] == 'Award Number') & (df['Unnamed: 1'] == 'Award Date'),
        lambda df: (pd.isna(df['Unnamed: 0']) == False) & df['Unnamed: 0'].str.contains('Total') & (pd.isna(df['Unnamed: 1']) == False) & (df['Unnamed: 1'] == ' ')
    )

    lastrow = datatable.iloc[len(datatable)-1]

    # get the vested quantity
    vested_qty = lastrow['Vested']
    
    # print("vested_qty:", vested_qty)

    return [['IBM', 'MORGAN', 'IBM-RSU', vested_qty, None]]



# sttmnt = pd.read_excel('../data/Copy of IBM_27Jan2021_101707.xls',  thousands=',')

# # print(sttmnt)

# print(MorganStockPlanIngress.transform_data(sttmnt))