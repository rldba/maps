# пакетное преобразование адресов в географические координаты
import os
from yandex_geocoder import Client
import pandas as pd

file_name = "~/PycharmProjects/maps/DataSets/cbr_str.xlsx"

pd.set_option('display.max_columns', None)

yandex_geo_api_key = os.environ.get("YandexGeoApiKey")

df_cbr_str = pd.read_excel(file_name)
df_cbr_str['LAT'] = 0.0
df_cbr_str['LON'] = 0.0

client = Client(yandex_geo_api_key)

for i, r in df_cbr_str.iterrows():
    result = client.coordinates(str(r['ADRESS']))
    if len(result) > 0:
            df_cbr_str.loc[i,'LON'], df_cbr_str.loc[i,'LAT'] = result

df_cbr_str = df_cbr_str.loc[df_cbr_str['LAT'] != 0]
df_cbr_str.reset_index(drop=True, inplace=True)
df_cbr_str.to_excel("~/PycharmProjects/maps/DataSets/cbr_str_geo.xlsx")
print(df_cbr_str)