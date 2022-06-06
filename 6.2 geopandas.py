# Геопандас / Cвердловская обл.
import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt
pd.set_option('display.max_columns', None)

#Свердловская обл общая граница
gpd_svd_L1 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl4.shp', encoding='utf-8')
# районы и округа 73 шт 65763000
gpd_svd_L2 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl6.shp', encoding='utf-8')
#сельские поселения 22 шт 65628420
gpd_svd_L3 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl8.shp', encoding='utf-8')
#населенные пункты 2272  шт 65755000141
gpd_svd_L4 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/settlement-point.shp', encoding='utf-8')

print(gpd_svd_L3.info())
print(gpd_svd_L3[['NAME', 'oktmo', 'geometry']])

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(10,5))
gpd_svd_L1.plot(ax=ax1, color='white', edgecolor='black')
gpd_svd_L2.plot(ax=ax2, color='white', edgecolor='black')
gpd_svd_L3.plot(ax=ax3, color='white', edgecolor='black')
gpd_svd_L4.plot(ax=ax4, color='white', edgecolor='black')
plt.show()