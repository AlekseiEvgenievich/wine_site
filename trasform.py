import pandas
from pprint import pprint
import numpy as np

excel_data_df = pandas.read_excel('wine3.xlsx')
excel_data_df.replace({np.nan: None}, inplace=True)
organized_data = excel_data_df.groupby('Категория').apply(lambda x: x.drop('Категория', axis=1).to_dict(orient='records')).to_dict()

print(organized_data)




