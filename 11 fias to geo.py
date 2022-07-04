# https://github.com/hflabs/dadata-py
# пакетное преобразование fias - кодов в географические координаты
import os
from dadata import Dadata
import pandas as pd

file_name = "~/PycharmProjects/maps/DataSets/svd/svd_sber_bk.xlsx"

pd.set_option('display.max_columns', None)

token = os.environ.get('DADATA_TOKEN')
secret = os.environ.get('DADATA_SECRET')

df_alfa_bk = pd.read_excel(file_name)
df_alfa_bk['LAT'] = 0.0
df_alfa_bk['LON'] = 0.0

with Dadata(token, secret) as dadata:
    for i, r in df_alfa_bk.iterrows():
        result = dadata.find_by_id("address",str(r['FIAS']))
        if len(result) > 0:
            print(i)
            df_alfa_bk.loc[i,'LAT'] = result[0]['data']['geo_lat']
            df_alfa_bk.loc[i,'LON'] = result[0]['data']['geo_lon']

df_alfa_bk = df_alfa_bk.loc[df_alfa_bk['LAT'] != 0]
df_alfa_bk.reset_index(drop=True, inplace=True)
df_alfa_bk.to_excel("~/PycharmProjects/maps/DataSets/svd/svd_sber_bk_geo.xlsx")
print(df_alfa_bk)