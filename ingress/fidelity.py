import pandas as pd
from util import ingressutil

class FidelityIngress:

  @staticmethod
  def is_valid(data_to_check: pd.DataFrame) -> bool:

    first_col_name = data_to_check.columns[0]
    return ('Account Name/Number' == first_col_name)


  @staticmethod
  def transform_data(statement: pd.DataFrame) -> []:
    
    # Find the first row that is the actual header row
    # Find the last row that ends the data table
    # Get the rows between header row and end row
    # Create a new table with new headers from the header row

    datatable = ingressutil.read_data_table(statement, None, None)

    # print('Fidelity datatable: ', datatable)

    poss = []

    # get the rows with positions (by checking Symbol column and it doesn't end with ** (which is cash))
    ass = datatable[pd.notna(datatable['Symbol']) & (datatable['Symbol'].str.endswith('**') == False)]

    for index, row in ass.iterrows():
      index
      poss.append([row['Symbol'], 'Fidelity', row['Account Name/Number'].strip(), float(row['Quantity']), float(row['Last Price'].replace('$', ''))])

    return poss

# sttmnt = pd.read_csv('../data/Copy of Portfolio_Positions_Jan-27-2021.csv',  thousands=',')

# print("is_valid: ", FidelityIngress.is_valid(sttmnt))
# print(FidelityIngress.transform_data(sttmnt))