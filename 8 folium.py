import geopandas as gpd
import pandas as pd
import json
import folium
from folium.plugins import MarkerCluster
import webbrowser
pd.set_option('display.max_columns', None)

# читаем шейп файл
#районы республики / 2 уровень 64 шт
gpd_bash_L2 = gpd.read_file('~/PycharmProjects/maps/GeoData/bash/boundary-polygon-lvl6.shp', encoding='utf-8')
# В геопанде oktmo должно быть  integer / проверяем и корректируем при необходимости
gpd_bash_L2.loc[(gpd_bash_L2['NAME'] == 'Фёдоровский район'),'oktmo'] = 80654000
gpd_bash_L2['oktmo'] = pd.to_numeric(gpd_bash_L2['oktmo'])
gpd_bash_L2['oktmo'] = gpd_bash_L2['oktmo']/1000
gpd_bash_L2['oktmo'] = pd.to_numeric(gpd_bash_L2['oktmo'],downcast='integer')
gpd_bash_L2 = gpd_bash_L2.loc[gpd_bash_L2['oktmo'] != 57735]
#print(gpd_bash_L2.info())

#населенные пункты / 4 уровень 4690 шт
gpd_bash_L4 = gpd.read_file('~/PycharmProjects/maps/GeoData/bash/settlement-point.shp', encoding='utf-8')
# В геопанде oktmo должно быть  integer / проверяем и корректируем при необходимости
gpd_bash_L4.loc[(gpd_bash_L4['oktmo'].isnull()),'oktmo'] = 0
gpd_bash_L4['oktmo'] = pd.to_numeric(gpd_bash_L4['oktmo'])
#отбираем только города 59 шт
gpd_bash_L4 = gpd_bash_L4.loc[gpd_bash_L4['PLACE'].isin(['town','city'])]
gpd_bash_L4.reset_index(drop=True, inplace=True)
#print(gpd_bash_L4)


# читаем эксель с данными по L2
df = pd.read_excel("~/PycharmProjects/maps/DataSets/bash/bash_level2.xlsx")
df['OKTMO'] = pd.to_numeric(df['OKTMO'],downcast='integer')
df['ATM'] = pd.to_numeric(df['ATM'],downcast='integer')
df['PEOPLE'] = pd.to_numeric(df['PEOPLE'],downcast='integer')
df['ATM1000PEOPLE'] = df['ATM']/df['PEOPLE']*1000
#print(df.info())

# добавляем данные из DataFrame в геопандадатафрейм
gpd_bash_L2['ATM1000PEOPLE'] = gpd_bash_L2['oktmo'].map(df.set_index('OKTMO')['ATM1000PEOPLE'])
gpd_bash_L2['ATM'] = gpd_bash_L2['oktmo'].map(df.set_index('OKTMO')['ATM'])
gpd_bash_L2['PEOPLE'] = gpd_bash_L2['oktmo'].map(df.set_index('OKTMO')['PEOPLE'])

#создаю карту
m = folium.Map(location=[54.771648, 56.026932], zoom_start=7, tiles='OpenStreetMap')

#******************************** СЛОЙ С ГРАНИЦАМИ РАЙОНОВ РЕСПУБЛИКИ И ПОДПИСЯМИ ************************************
layer_bash_L2 = folium.FeatureGroup(name='Республика Башкортостан (L2)')

for _, r in gpd_bash_L2.iterrows():
    # Без упрощения представления каждого района карта может не отображаться
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j,
                           style_function=lambda x: {'fillColor': '#00000000', 'color': 'grey', 'weight': 1}) #'fillColor': 'orange',
    geo_j_info =  '<b>' + str(r['NAME']) + '</b>'
    geo_j_stat = f"Жителей:_{str(r['PEOPLE'])}_чел. ATM:_{str(r['ATM'])}_шт."
    folium.Popup(geo_j_stat).add_to(geo_j) # подсказки статика по клику мыши
    folium.Tooltip(geo_j_info).add_to(geo_j) # подсказки всплывающие при наведении мыши
    layer_bash_L2.add_child(geo_j)

layer_bash_L2.add_to(m)
#*****************************************************************************************

#******************************** СЛОИ С населенными пуктами РЕСПУБЛИКИ И ПОДПИСЯМИ ************************************

# Create a geometry list from the GeoDataFrame
# Получаем перечень координат населенных пунктов из  GeoPand'ы
dl_bash_L4_point = [[point.xy[1][0], point.xy[0][0]] for point in gpd_bash_L4.geometry]

layer_bash_L4_point = folium.FeatureGroup(name='Населенные пункты v1 (L4)', show = False)
i = 0
for coordinates in dl_bash_L4_point:
  geo_j = folium.CircleMarker(location = coordinates,
                            tooltip = str(gpd_bash_L4['NAME'][i]),
                            radius = 5, fill_color = 'yellow' ,color = 'gray', fill_opacity = 0.9)
  layer_bash_L4_point.add_child(geo_j)
  i = i + 1
layer_bash_L4_point.add_to(m)

layer_bash_L4_cluster_point = MarkerCluster(name='Населенные пункты v2 (L4)', show = False)
i = 0
for coordinates in dl_bash_L4_point:
  geo_j = folium.CircleMarker(location = coordinates,
                            tooltip = str(gpd_bash_L4['NAME'][i]),
                            radius = 5, fill_color = 'yellow' ,color = 'gray', fill_opacity = 0.9)
  layer_bash_L4_cluster_point.add_child(geo_j)
  i = i + 1
layer_bash_L4_cluster_point.add_to(m)

layer_bash_L4_cluster_maps_point = MarkerCluster(name='Населенные пункты v3 (L4)', show = False)

i = 0
for coordinates in dl_bash_L4_point:
  geo_j = folium.Marker(location = coordinates,
                            icon = folium.Icon(icon = 'fa-circle', icon_color = 'black', prefix='fa', color = 'green'),
                            tooltip = str(gpd_bash_L4['NAME'][i]))
  layer_bash_L4_cluster_maps_point.add_child(geo_j)
  i = i + 1
layer_bash_L4_cluster_maps_point.add_to(m)

#******************************** СЛОЙ С ТЕПЛОВОЙ КАРТОЙ ************************************
# Фоновая картограмма или хороплет (от греч. χώρο- + πλήθ[ος], «место, область» + «значение») — вид картограммы,
# на которой штриховкой различной густоты или краской разной степени насыщенности
# изображают интенсивность какого-либо показателя в пределах территориальной единицы.

# преобразую из geopandas в geo_json формат
geo_data_json_bash_L2 = gpd_bash_L2.to_json()
geo_data_json_bash_L2 = json.loads(geo_data_json_bash_L2)

#создаем слой хороплета
layer_choropleth_bash_l2 = folium.Choropleth(
       geo_data = geo_data_json_bash_L2,
       name = 'Плотность сети банкоматов',
       data = df,
       columns=['OKTMO', 'ATM1000PEOPLE'], #из DataFrame
       key_on='feature.properties.oktmo', # из GeoJSON
       bins = 8,
       fill_color='Blues',
       nan_fill_color='darkblue',
       nan_fill_opacity=0.5,
       fill_opacity=0.6,
       line_opacity=0.2,
       legend_name= 'Количество банкоматов на тыс. жителей',
       highlight = True,
       show = False
)
layer_choropleth_bash_l2.add_to(m)
#*****************************************************************************************

m.keep_in_front(layer_choropleth_bash_l2,layer_bash_L2,layer_bash_L4_point,layer_bash_L4_cluster_point,layer_bash_L4_cluster_maps_point)
controlLayers = folium.LayerControl(autoZIndex=False, name = 'test')
controlLayers.add_to(m)

#отображаем карту
m.save('results/map.html')
webbrowser.open('/results/map.html')

