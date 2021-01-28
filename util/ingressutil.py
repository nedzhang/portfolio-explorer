import io
import pandas as pd


def __slice_rows(data: pd.DataFrame, startrow: pd.DataFrame, endrow: pd.DataFrame) -> pd.DataFrame:
  min_ind = min(startrow.index.tolist() or [0])
  max_ind = max(endrow.index.tolist() or [len(data)])
  # this method assumes we are using an index that increments by 1
  return data[min_ind:max_ind+1]


def __convert_to_new_table(datarows: pd.DataFrame) -> pd.DataFrame:

  s_buf = io.StringIO()

  datarows.to_csv(s_buf, header=False, index=False)
  s_buf.seek(0)
  newtable = pd.read_csv(s_buf)

  return newtable


### Read a section of dataframe as a table ###
def read_data_table(rawtable: pd.DataFrame, headercondition, endcondition) -> pd.DataFrame:

  if (headercondition is None and endcondition is None):
    # Use the raw table as is since there is no condition
    return rawtable
  else:
    # Find the first row that is the actual header row
    headerrow = rawtable[headercondition]
    # Find the last row that ends the data table
    lastrow = rawtable[endcondition]
    # Get the rows between header row and end row
    datarows = __slice_rows(rawtable, headerrow, lastrow)
    # Create a new table with new headers from the header row
    datatable = __convert_to_new_table(datarows)

    # print("headerrow:\n", headerrow)
    # print("lastrow:\n", lastrow)
    # print("data:\n", datarows)

    return datatable

