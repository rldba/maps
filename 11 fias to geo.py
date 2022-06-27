# https://github.com/hflabs/dadata-py
import os
from dadata import Dadata
import pandas as pd

pd.set_option('display.max_columns', None)

token = os.environ.get('DADATA_TOKEN')
secret = os.environ.get('DADATA_SECRET')

df_alfa_bk = pd.read_excel("~/PycharmProjects/maps/DataSets/svd/svd_alfa_bk.xlsx")
df_alfa_bk['LAT'] = 0.0
df_alfa_bk['LON'] = 0.0

print(df_alfa_bk.info())
print(df_alfa_bk[0:1])

# with Dadata(token, secret) as dadata:
    # result = dadata.find_by_id("address", "0ccdcb1e-6fea-4590-b3ff-a226991d4f19")
    # print(result)
    # print(result[0]['data']['geo_lat'])
    # print(result[0]['data']['geo_lon'])

#     for i, r in df_alfa_bk.iterrows():
#         result = dadata.find_by_id("address",str(r['FIAS']))
#         print(result)
#         print(len(result))
#         if len(result) > 0:
#             print(result[0]['data']['geo_lat'])
#             print(result[0]['data']['geo_lon'])
#             print(i)
#             df_alfa_bk[i]['LAT'] = result[0]['data']['geo_lat']
#             r['LON'] = result[0]['data']['geo_lon']
#
# print(df_alfa_bk)
