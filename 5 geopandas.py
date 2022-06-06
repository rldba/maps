# Геопандас / начало / шейп файл регионов России

import geopandas as gpd
from matplotlib import pyplot as plt

gpd_Russia_L1 = gpd.read_file('~/PycharmProjects/maps/GeoData/ru/gadm36_RUS_1.shp', encoding='utf-8')

print(gpd_Russia_L1.info())

print(gpd_Russia_L1[["NL_NAME_1","geometry"]])

gpd_Russia_L1.plot(color="white",edgecolor='black', linewidth=1)
plt.show()

# gpd_UGU_L1=gpd_Russia_L1.loc[gpd_Russia_L1['NAME_1'].isin(['Chelyabinsk','Orenburg',"Perm'","Tyumen'",'Kurgan','Bashkortostan','Sverdlovsk'])] #'Bashkortostan',"Sverdlovsk"
# print(gpd_UGU_L1[["NL_NAME_1","geometry"]])
# gpd_UGU_L1.plot(color="white",edgecolor='black', linewidth=1)
# plt.show()
