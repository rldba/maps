import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt
# pd.set_option('display.max_columns', None)

# читаем шейп файл
#районы республики / 2 уровень 64 шт
gpd_bash_L2 = gpd.read_file('~/PycharmProjects/maps/GeoData/bash/boundary-polygon-lvl6.shp', encoding='utf-8')

# В геопанде oktmo должно быть  integer / проверяем и корректируем при необходимости
gpd_bash_L2.loc[(gpd_bash_L2['NAME'] == 'Фёдоровский район'),'oktmo'] = 80654000
gpd_bash_L2['oktmo'] = pd.to_numeric(gpd_bash_L2['oktmo'])
gpd_bash_L2['oktmo'] = gpd_bash_L2['oktmo']/1000
gpd_bash_L2['oktmo'] = pd.to_numeric(gpd_bash_L2['oktmo'],downcast='integer')
print(gpd_bash_L2.info())

# читаем эксель с данными по L2
df = pd.read_excel("~/PycharmProjects/maps/DataSets/bash/bash_level2.xlsx")
df['OKTMO'] = pd.to_numeric(df['OKTMO'],downcast='integer')
df['ATM1000PEOPLE'] = df['ATM']/df['PEOPLE']*1000
print(df.info())

# добавляем данные по плотности в геопандадатафрейм **************************************************************
gpd_bash_L2['PLOTN'] = gpd_bash_L2['oktmo'].map(df.set_index('OKTMO')['PLOTN'])
gpd_bash_L2['ATM1000PEOPLE'] = gpd_bash_L2['oktmo'].map(df.set_index('OKTMO')['ATM1000PEOPLE'])

print(gpd_bash_L2[["NAME","ATM1000PEOPLE"]])

# рисуем карту / можно подписать города
fig, ax1 = plt.subplots(1, 1, figsize=(10,7))
gpd_bash_L2.plot(column='ATM1000PEOPLE',edgecolor='black', linewidth=1, ax=ax1, legend=True, cmap='YlGn') # https://matplotlib.org/2.0.2/users/colormaps.html
plt.axis('off')
plt.title("Количество банкоматов на тыс. жителей по районам Республикм Башкортостан")
plt.show()

