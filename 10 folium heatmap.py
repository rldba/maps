import geopandas as gpd
import pandas as pd
import json
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from folium.plugins import LocateControl
from folium.plugins import MeasureControl

import webbrowser
pd.set_option('display.max_columns', None)

#******************************** ЧИТАЕМ ШЕЙП ФАЙЛЫ ПО РБ и Свердловской обл. ************************************
#Республика Башкортостан
gpd_bash_L1 = gpd.read_file('~/PycharmProjects/maps/GeoData/bash/boundary-polygon-lvl4.shp', encoding='utf-8')
#районы республики / 2 уровень 64 шт
gpd_bash_L2 = gpd.read_file('~/PycharmProjects/maps/GeoData/bash/boundary-polygon-lvl6.shp', encoding='utf-8')
#муниципальные образования / 3 уровень 832 шт
gpd_bash_L3 = gpd.read_file('~/PycharmProjects/maps/GeoData/bash/boundary-polygon-lvl8.shp', encoding='utf-8')
#населенные пункты / 4 уровень 4690 шт
gpd_bash_L4 = gpd.read_file('~/PycharmProjects/maps/GeoData/bash/settlement-point.shp', encoding='utf-8')

#Свердловская обл общая граница
gpd_svd_L1 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl4.shp', encoding='utf-8')
# районы и округа 73 шт 65763000
gpd_svd_L2 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl6.shp', encoding='utf-8')
#сельские поселения 22 шт 65628420
gpd_svd_L3 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl8.shp', encoding='utf-8')
#населенные пункты 2272  шт 65755000141
gpd_svd_L4 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/settlement-point.shp', encoding='utf-8')

#******************************** Верификация / очистка / загруженых данных ************************************
# В геопанде oktmo должно быть  integer / проверяем и корректируем при необходимости
gpd_bash_L2.loc[(gpd_bash_L2['NAME'] == 'Фёдоровский район'),'oktmo'] = 80654000
gpd_bash_L2['oktmo'] = pd.to_numeric(gpd_bash_L2['oktmo'])
gpd_bash_L2['oktmo'] = gpd_bash_L2['oktmo']/1000
gpd_bash_L2['oktmo'] = pd.to_numeric(gpd_bash_L2['oktmo'],downcast='integer')
gpd_bash_L2 = gpd_bash_L2.loc[gpd_bash_L2['oktmo'] != 57735]
#print(gpd_bash_L2.info())
gpd_bash_L3.loc[(gpd_bash_L3['OSM_ID'] == 8324081),'oktmo'] = 80255850
gpd_bash_L3.loc[(gpd_bash_L3['OSM_ID'] == 8322315),'oktmo'] = 80206842
gpd_bash_L3.loc[(gpd_bash_L3['OSM_ID'] == 8309502),'oktmo'] = 80237821
gpd_bash_L3.loc[(gpd_bash_L3['OSM_ID'] == 8278901),'oktmo'] = 80202806
gpd_bash_L3.loc[(gpd_bash_L3['OSM_ID'] == 8028015),'oktmo'] = 80654460
gpd_bash_L3.loc[(gpd_bash_L3['OSM_ID'] == 8028009),'oktmo'] = 80654430
gpd_bash_L3.loc[(gpd_bash_L3['OSM_ID'] == 8028019),'oktmo'] = 80654440
gpd_bash_L3['oktmo'] = pd.to_numeric(gpd_bash_L3['oktmo'])
#print(gpd_bash_L3.info())
gpd_bash_L4.loc[(gpd_bash_L4['oktmo'].isnull()),'oktmo'] = 0
gpd_bash_L4['oktmo'] = pd.to_numeric(gpd_bash_L4['oktmo'])
#print(gpd_bash_L4.info())

gpd_svd_L2.loc[(gpd_svd_L2['NAME'] == 'Камышловский район'),'oktmo'] = 65623000
gpd_svd_L2['oktmo'] = pd.to_numeric(gpd_svd_L2['oktmo'])
gpd_svd_L2['oktmo'] = gpd_svd_L2['oktmo']/1000
gpd_svd_L2['oktmo'] = pd.to_numeric(gpd_svd_L2['oktmo'],downcast='integer')
#print(gpd_svd_L2.info())
gpd_svd_L3['oktmo'] = pd.to_numeric(gpd_svd_L3['oktmo'])
#print(gpd_svd_L3.info())
gpd_svd_L4.loc[(gpd_svd_L4['oktmo'].isnull()),'oktmo'] = 0
gpd_svd_L4['oktmo'] = pd.to_numeric(gpd_svd_L4['oktmo'])
#print(gpd_svd_L4.info())

#******************************** ОБЪЕДИНЯЕМ ГЕОПАНДЫ В ЕДИНОЕ ПРОСТРАНСТВО ************************************
gpd_L2 = pd.concat([gpd_bash_L2, gpd_svd_L2])
gpd_L3 = pd.concat([gpd_bash_L3, gpd_svd_L3])
gpd_L4 = pd.concat([gpd_bash_L4, gpd_svd_L4])
gpd_L4.reset_index(drop=True, inplace=True)

#******************************** читаем эксель с данными по L2 ************************************
df_bash_L2 = pd.read_excel("~/PycharmProjects/maps/DataSets/bash/bash_level2.xlsx")
df_bash_L2['OKTMO'] = pd.to_numeric(df_bash_L2['OKTMO'],downcast='integer')
df_bash_L2['ATM'] = pd.to_numeric(df_bash_L2['ATM'],downcast='integer')
df_bash_L2['PEOPLE'] = pd.to_numeric(df_bash_L2['PEOPLE'],downcast='integer')
df_bash_L2['ATM1000PEOPLE'] = df_bash_L2['ATM']/df_bash_L2['PEOPLE']*1000

df_svd_L2 = pd.read_excel("~/PycharmProjects/maps/DataSets/svd/svd_level2.xlsx")
df_svd_L2['OKTMO'] = pd.to_numeric(df_svd_L2['OKTMO'],downcast='integer')
df_svd_L2['ATM'] = pd.to_numeric(df_svd_L2['ATM'],downcast='integer')
df_svd_L2['PEOPLE'] = pd.to_numeric(df_svd_L2['PEOPLE'],downcast='integer')
df_svd_L2['ATM1000PEOPLE'] = df_svd_L2['ATM']/df_svd_L2['PEOPLE']*1000

#******************************** читаем эксель с данными по L4 ************************************
df_bash_L4 = pd.read_excel("~/PycharmProjects/maps/DataSets/bash/bash_level4.xlsx")
df_bash_L4['OKTMO'] = pd.to_numeric(df_bash_L4['OKTMO'],downcast='integer')
df_bash_L4['ATM'] = pd.to_numeric(df_bash_L4['ATM'],downcast='integer')
df_bash_L4['POS_TERM'] = pd.to_numeric(df_bash_L4['POS_TERM'],downcast='integer')
df_bash_L4['PEOPLE'] = pd.to_numeric(df_bash_L4['PEOPLE'],downcast='integer')
df_bash_L4['ATM1000PEOPLE'] = df_bash_L4['ATM']/df_bash_L4['PEOPLE']*1000

df_svd_L4 = pd.read_excel("~/PycharmProjects/maps/DataSets/svd/svd_level4.xlsx")
df_svd_L4['OKTMO'] = pd.to_numeric(df_svd_L4['OKTMO'],downcast='integer')
df_svd_L4['ATM'] = pd.to_numeric(df_svd_L4['ATM'],downcast='integer')
df_svd_L4['POS_TERM'] = pd.to_numeric(df_svd_L4['POS_TERM'],downcast='integer')
df_svd_L4['PEOPLE'] = pd.to_numeric(df_svd_L4['PEOPLE'],downcast='integer')
df_svd_L4['ATM1000PEOPLE'] = df_svd_L4['ATM']/df_svd_L4['PEOPLE']*1000

#******************************** ОБЪЕДИНЯЕМ DataFrame ************************************
df_l2 = pd.concat([df_bash_L2, df_svd_L2])
df_l4 = pd.concat([df_bash_L4, df_svd_L4])

# добавляем данные из DataFrame в геопандадатафрейм
gpd_L2['ATM1000PEOPLE'] = gpd_L2['oktmo'].map(df_l2.set_index('OKTMO')['ATM1000PEOPLE'])
gpd_L2['ATM'] = gpd_L2['oktmo'].map(df_l2.set_index('OKTMO')['ATM'])
gpd_L2['PEOPLE'] = gpd_L2['oktmo'].map(df_l2.set_index('OKTMO')['PEOPLE'])

gpd_L4['ATM1000PEOPLE'] = gpd_L4['oktmo'].map(df_l4.set_index('OKTMO')['ATM1000PEOPLE'])
gpd_L4['ATM'] = gpd_L4['oktmo'].map(df_l4.set_index('OKTMO')['ATM'])
gpd_L4['POS_TERM'] = gpd_L4['oktmo'].map(df_l4.set_index('OKTMO')['POS_TERM'])
gpd_L4['PEOPLE'] = gpd_L4['oktmo'].map(df_l4.set_index('OKTMO')['PEOPLE'])

gpd_L4.loc[(gpd_L4['POS_TERM'].isnull()),'POS_TERM'] = 0
gpd_L4.loc[(gpd_L4['PEOPLE'].isnull()),'PEOPLE'] = 0
gpd_L4['POS_TERM'] = pd.to_numeric(gpd_L4['POS_TERM'],downcast='integer')
gpd_L4['PEOPLE'] = pd.to_numeric(gpd_L4['PEOPLE'],downcast='integer')
# print(gpd_L4.info())

#******************************** отбираем только города 132 шт получится************************************
gpd_L4_city = gpd_L4.loc[gpd_L4['PLACE'].isin(['town','city'])]
gpd_L4_city.reset_index(drop=True, inplace=True)


#создаю карту
m = folium.Map(location=[56.838924, 60.605701], zoom_start=6, tiles='OpenStreetMap')
folium.TileLayer('CartoDB positron').add_to(m)
folium.TileLayer('CartoDB dark_matter').add_to(m)

#******************************** СЛОЙ С ГРАНИЦАМИ РАЙОНОВ И ОКРУГОВ С ПОДПИСЯМИ ************************************
layer_L2 = folium.FeatureGroup(name='Районы и округа (L2)')

for _, r in gpd_L2.iterrows():
    # Без упрощения представления каждого района карта может не отображаться
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j,
                           style_function=lambda x: {'fillColor': '#00000000', 'color': 'grey', 'weight': 1}) #'fillColor': 'orange',
    geo_j_info =  '<b>' + str(r['NAME']) + '</b>'
    folium.Tooltip(geo_j_info).add_to(geo_j) # подсказки всплывающие при наведении мыши
    geo_j_stat = f"Жителей:_{str(r['PEOPLE'])}_чел. ATM:_{str(r['ATM'])}_шт."
    folium.Popup(geo_j_stat).add_to(geo_j) # подсказки статика по клику мыши
    layer_L2.add_child(geo_j)

layer_L2.add_to(m)


#******************************** СЛОЙ С населенными пуктами И ПОДПИСЯМИ ************************************

# Create a geometry list from the GeoDataFrame
# Получаем перечень координат населенных пунктов из  GeoPand'ы
dl_L4 = [[point.xy[1][0], point.xy[0][0]] for point in gpd_L4.geometry]

layer_L4 = MarkerCluster(name='Населенные пункты все (L4)', show = False)
i = 0
for coordinates in dl_L4:
  geo_j = folium.CircleMarker(location = coordinates,
                            tooltip = f"{gpd_L4['NAME'][i]}<br/>{gpd_L4['PEOPLE'][i]} жителей<br/>{gpd_L4['POS_TERM'][i]} POS-терминалов",
                            radius = 3, fill_color = 'yellow' ,color = 'gray', fill_opacity = 0.9)
  layer_L4.add_child(geo_j)
  i = i + 1
layer_L4.add_to(m)

#******************************** СЛОЙ С крупными населенными пуктами И ПОДПИСЯМИ ************************************

# Create a geometry list from the GeoDataFrame
# Получаем перечень координат населенных пунктов из  GeoPand'ы
dl_L4_city = [[point.xy[1][0], point.xy[0][0]] for point in gpd_L4_city.geometry]

layer_L4_city = folium.FeatureGroup(name='Крупные населенные пункты (L4)', show = False)
i = 0
for coordinates in dl_L4_city:
  geo_j = folium.CircleMarker(location = coordinates,
                            tooltip = f"{gpd_L4_city['NAME'][i]}<br/>{gpd_L4_city['PEOPLE'][i]} жителей<br/>{gpd_L4_city['POS_TERM'][i]} POS-терминалов",
                            radius = 5, fill_color = 'yellow' ,color = 'gray', fill_opacity = 0.9)
  layer_L4_city.add_child(geo_j)
  i = i + 1
layer_L4_city.add_to(m)


#******************************** HEAT MAP layer ************************************
# Получаем перечень координат населенных пунктов из  GeoPand'ы
#data=df_copy[['pickup_latitude', 'pickup_longitude', 'count']].groupby(['pickup_latitude', 'pickup_longitude']).sum().reset_index().values.tolist()
#dl_L4 = [[point.xy[1][0], point.xy[0][0]] for point in gpd_L4_city.geometry]
gpd_L4['lat'] = gpd_L4.geometry.x
gpd_L4['lon'] = gpd_L4.geometry.y

gpd_L4_not_null = gpd_L4.loc[gpd_L4['POS_TERM'] != 0]
# Create a geometry list x,y,value from the GeoDataFrame
dl_L4 = gpd_L4_not_null[['lon','lat','POS_TERM']].values.tolist()

# print(gpd_L4_city)
#print(dl_L4)

# Available parameters: HeatMap(data, name=None, min_opacity=0.5, max_zoom=18, max_val=1.0, radius=25, blur=15, gradient=None, overlay=True, control=True, show=True)
layer_L5 = HeatMap(dl_L4, name='Количество POS-терминалов (HeatMap)', show = False, radius=20, gradient={.3: 'red', .5: 'yellow', 1: 'green'},min_opacity=0.3)

layer_L5.add_to(m)

controlLayers = folium.LayerControl(autoZIndex=False, name = 'test')
controlLayers.add_to(m)
#контроллер локации
LocateControl().add_to(m)

MeasureControl(position='bottomright', primary_length_unit='meters').add_to(m)

#отображаем карту
m.save('results/map.html')
webbrowser.open('/results/map.html')
