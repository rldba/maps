# https://github.com/hflabs/dadata-py
# пакетное преобразование fias - кодов в географические координаты
import os
from dadata import Dadata
import pandas as pd

file_name = "~/PycharmProjects/maps/DataSets/oktmo.xlsx"

pd.set_option('display.max_columns', None)

token = os.environ.get('DADATA_TOKEN')
secret = os.environ.get('DADATA_SECRET')

df_oktmo = pd.read_excel(file_name)
df_oktmo['ADRESS'] = ""
df_oktmo['LAT'] = 0.0
df_oktmo['LON'] = 0.0


with Dadata(token, secret) as dadata:
    # result = dadata.find_by_id("address", str(df_oktmo.loc[1,'fias'])) #'oktmo': '80618416151'
    # print (result)
    # print (result[0]['data']['oktmo'])
    # print (result[0]['unrestricted_value'])
    for i, r in df_oktmo.iterrows():
        result = dadata.find_by_id("address",str(r['fias']))
        if len(result) > 0:
            print(i)
            df_oktmo.loc[i,'LAT'] = result[0]['data']['geo_lat']
            df_oktmo.loc[i,'LON'] = result[0]['data']['geo_lon']
            df_oktmo.loc[i,'oktmo'] = result[0]['data']['oktmo']
            df_oktmo.loc[i,'ADRESS'] = result[0]['unrestricted_value']

#df_alfa_bk = df_alfa_bk.loc[df_alfa_bk['LAT'] != 0]
#df_alfa_bk.reset_index(drop=True, inplace=True)
df_oktmo.to_excel("~/PycharmProjects/maps/DataSets/oktmo_result.xlsx")
print(df_oktmo)
