# Геопандас / Башкортостан
import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt
pd.set_option('display.max_columns', None)

#Республика Башкортостан
gpd_bash_L1 = gpd.read_file('~/PycharmProjects/maps/GeoData/bash/boundary-polygon-lvl4.shp', encoding='utf-8')
#районы республики / 2 уровень 64 шт
gpd_bash_L2 = gpd.read_file('~/PycharmProjects/maps/GeoData/bash/boundary-polygon-lvl6.shp', encoding='utf-8')
#муниципальные образования / 3 уровень 832 шт
gpd_bash_L3 = gpd.read_file('~/PycharmProjects/maps/GeoData/bash/boundary-polygon-lvl8.shp', encoding='utf-8')
#населенные пункты / 4690 шт
gpd_bash_L4 = gpd.read_file('~/PycharmProjects/maps/GeoData/bash/settlement-point.shp', encoding='utf-8')

print(gpd_bash_L3.info())
print(gpd_bash_L3[['NAME', 'oktmo', 'geometry']])

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(10,5))
gpd_bash_L1.plot(ax=ax1, color='white', edgecolor='black') #Республика Башкортостан
gpd_bash_L2.plot(ax=ax2, color='white', edgecolor='black') #районы республики / 2 уровень 64 шт
gpd_bash_L3.plot(ax=ax3, color='white', edgecolor='black') #муниципальные образования / 3 уровень 832 шт
gpd_bash_L4.plot(ax=ax4, color='white', edgecolor='black') #сельские поселения
plt.show()