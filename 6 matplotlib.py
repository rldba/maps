# Геопандас / начало / тепловая карта УГУ

import geopandas as gpd
import shapely
import pandas as pd
from matplotlib import pyplot as plt
# pd.set_option('display.max_columns', None)

# читаем шейп файл
gpd_Russia_L1 = gpd.read_file('~/PycharmProjects/maps/GeoData/ru/gadm36_RUS_1.shp', encoding='utf-8')
# отбираем только регионы УГУ
gpd_UGU_L1=gpd_Russia_L1.loc[gpd_Russia_L1['NAME_1'].isin(['Chelyabinsk','Orenburg',"Perm'","Tyumen'",'Kurgan','Bashkortostan','Sverdlovsk'])] #'Bashkortostan',"Sverdlovsk"
print(gpd_UGU_L1[["NAME_1","geometry"]])
# читаем эксель с данными по заражениям Ковидом
df = pd.read_excel("~/PycharmProjects/maps/DataSets/region_stats.xlsx")
print(df)
# добавляем данные по заражению ковидом и прочие в геопандадатафрейм
gpd_UGU_L1['COVID_100000'] = gpd_UGU_L1['NAME_1'].map(df.set_index('REGION')['COVID_100000'])
gpd_UGU_L1['KREDIT'] = gpd_UGU_L1['NAME_1'].map(df.set_index('REGION')['KREDIT'])
gpd_UGU_L1['INT_INVEST'] = gpd_UGU_L1['NAME_1'].map(df.set_index('REGION')['INT_INVEST'])
# print(gpd_UGU_L1[["NAME_1","COVID_100000"]])
# считаем процент зараженных
gpd_UGU_L1['COVID_percent'] = gpd_UGU_L1['COVID_100000'] / 1000
# print(gpd_UGU_L1[["NAME_1","COVID_percent"]])

# создаем датафрейм с региональными столицами
df_city = pd.DataFrame({'city': ['Екатеринбург', 'Пермь', 'Тюмень', 'Курган', 'Оренбург', 'Челябинск', 'Уфа'],
                        'latitude': [56.838924, 58.029682, 57.156727, 55.456180, 51.768955, 55.163769, 54.771648],
                        'longitude': [60.605701, 56.266792, 65.542508, 65.322805, 55.096627, 61.399334, 56.026932]})
# создаем геопанду с региональными столицами
gpd_city = gpd.GeoDataFrame(df_city.drop(['latitude', 'longitude'], axis=1),
                       crs={'init': 'epsg:4326'},
                       geometry=[shapely.geometry.Point(xy)
                                 for xy in zip(df_city.longitude, df_city.latitude)])
print(gpd_city)

# рисуем карту можно подписать города
fig, ax1 = plt.subplots(1, 1, figsize=(10,7))

# plt.title("Процент переболевших короной в регионах Уральского ГУ")
# gpd_UGU_L1.plot(column='COVID_percent',edgecolor='black', linewidth=1, ax=ax1, legend=True, cmap='OrRd') # https://matplotlib.org/2.0.2/users/colormaps.html

# plt.title("Соотношение среднедушевого долга по кредитам и годовой зарплаты в 2021 г., %")
# gpd_UGU_L1.plot(column='KREDIT',edgecolor='black', linewidth=1, ax=ax1, legend=True, cmap='GnBu') # https://matplotlib.org/2.0.2/users/colormaps.html

plt.title("Поступление прямых иностранных инвестиций в 2020г., млн.$USD")
gpd_UGU_L1.plot(column='INT_INVEST',edgecolor='black', linewidth=1, ax=ax1, legend=True, cmap='Greens') # https://matplotlib.org/2.0.2/users/colormaps.html

# gpd_city.plot(ax=ax1, marker='o', color='black', markersize=15)
bbox_props = dict(boxstyle="round", fc="w", ec="1", alpha=0.5)
for idx,dat in df_city.iterrows():
    ax1.scatter(dat.longitude, dat.latitude, s=20, color='black')
    ax1.annotate(dat.city, (dat.longitude, dat.latitude), color='black', size=12, bbox=bbox_props)
plt.axis('off')
plt.show()

