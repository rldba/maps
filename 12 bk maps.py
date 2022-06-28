import geopandas as gpd
import pandas as pd
import folium
import webbrowser
from folium.plugins import MarkerCluster
pd.set_option('display.max_columns', None)

#Свердловская обл общая граница
gpd_svd_L1 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl4.shp', encoding='utf-8')
# районы и округа 73 шт 65763000
gpd_svd_L2 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl6.shp', encoding='utf-8')
#сельские поселения 22 шт 65628420
gpd_svd_L3 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl8.shp', encoding='utf-8')
#населенные пункты 2272  шт 65755000141
gpd_svd_L4 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/settlement-point.shp', encoding='utf-8')

#******************************** Верификация / очистка / загруженых данных ************************************
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
gpd_L2 = gpd_svd_L2
gpd_L3 = gpd_svd_L3
gpd_L4 = gpd_svd_L4

#******************************** отбираем только города 132 шт получится************************************
gpd_L4_city = gpd_L4.loc[gpd_L4['PLACE'].isin(['town','city'])]
gpd_L4_city.reset_index(drop=True, inplace=True)

#******************************** читаем эксель с данными по бонкоматам ************************************
df_alfa_bk = pd.read_excel('~/PycharmProjects/maps/DataSets/svd/svd_alfa_bk_geo.xlsx')
df_vtb_bk = pd.read_excel('~/PycharmProjects/maps/DataSets/svd/svd_vtb_bk_geo.xlsx')
df_sber_bk = pd.read_excel('~/PycharmProjects/maps/DataSets/svd/svd_sber_bk_geo.xlsx')

#******************************** отбираем только один муниципальный район - Первоуральск************************************
oktmo_2lvl = 753
df_sber_bk = df_sber_bk.loc[df_sber_bk['OKTMO2'] == oktmo_2lvl]
df_vtb_bk = df_vtb_bk.loc[df_vtb_bk['OKTMO2'] == oktmo_2lvl]
df_alfa_bk = df_alfa_bk.loc[df_alfa_bk['OKTMO2'] == oktmo_2lvl]

df_sber_bk.reset_index(drop=True, inplace=True)
df_vtb_bk.reset_index(drop=True, inplace=True)
df_alfa_bk.reset_index(drop=True, inplace=True)

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
                           style_function=lambda x: {'fillColor': '#00000000', 'color': 'orange', 'weight': 1}) #'fillColor': 'orange',
    geo_j_info =  '<b>' + str(r['NAME']) + '</b>'
    folium.Tooltip(geo_j_info).add_to(geo_j) # подсказки всплывающие при наведении мыши
    layer_L2.add_child(geo_j)

layer_L2.add_to(m)
#*****************************************************************************************

#******************************** СЛОЙ С ГРАНИЦАМИ МУНИЦИПАЛЬНЫХ ОБРАЗОВАНИЙ И СЕЛЬСКИХ ПОСЕЛЕНИЙ С ПОДПИСЯМИ ************************************
layer_L3 = folium.FeatureGroup(name='МО и СП (L3)',show = False)

for _, r in gpd_L3.iterrows():
    # Без упрощения представления каждого района карта может не отображаться
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j,
                           style_function=lambda x: {'fillColor': '#00000000', 'color': 'grey', 'weight': 1}) #'fillColor': 'orange',
    geo_j_info =  '<b>' + str(r['NAME']) + '</b>'
    #geo_j_stat = f"Жителей:_{str(r['PEOPLE'])}_чел. ATM:_{str(r['ATM'])}_шт."
    #folium.Popup(geo_j_stat).add_to(geo_j) # подсказки статика по клику мыши
    folium.Tooltip(geo_j_info).add_to(geo_j) # подсказки всплывающие при наведении мыши
    layer_L3.add_child(geo_j)

layer_L3.add_to(m)
#*****************************************************************************************

#******************************** СЛОЙ С населенными пуктами И ПОДПИСЯМИ ************************************

# Create a geometry list from the GeoDataFrame
# Получаем перечень координат населенных пунктов из  GeoPand'ы
dl_L4_city = [[point.xy[1][0], point.xy[0][0]] for point in gpd_L4_city.geometry]

layer_L4 = folium.FeatureGroup(name='Населенные пункты (L4)', show = False)
i = 0
for coordinates in dl_L4_city:
  geo_j = folium.CircleMarker(location = coordinates,
                            tooltip = str(gpd_L4_city['NAME'][i]),
                            radius = 5, fill_color = 'yellow' ,color = 'gray', fill_opacity = 0.9)
  layer_L4.add_child(geo_j)
  i = i + 1
layer_L4.add_to(m)

#******************************** СЛОЙ С бонкоматами Alfa ************************************

icon_url = '/Users/ruslan/PycharmProjects/maps/img/alfabank_web_logo.png'
#layer_alfa = MarkerCluster(name='Alfa Bank', show=False)
layer_alfa = folium.FeatureGroup(name='Alfa Bank', show = False)

for i, r in df_alfa_bk.iterrows():
    icon = folium.features.CustomIcon(icon_url, icon_size=(20, 28))  # Creating a custom Icon
    alfa_point = folium.Marker(location=[df_alfa_bk.loc[i,'LAT'], df_alfa_bk.loc[i,'LON']],  # координаты маркера
                                      tooltip=df_alfa_bk.loc[i,'PLACE'],  # всплывающая подсказка
                                      icon=icon,
                                      popup=df_alfa_bk.loc[i,'VIDOP']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    alfa_point.add_to(layer_alfa)
layer_alfa.add_to(m)


#*****************************************************************************************

#******************************** СЛОЙ С бонкоматами vtb ************************************

icon_url = '/Users/ruslan/PycharmProjects/maps/img/vtb_web_logo.png'
#layer_alfa = MarkerCluster(name='Alfa Bank', show=False)
layer_vtb = folium.FeatureGroup(name='VTB Bank', show = False)

for i, r in df_vtb_bk.iterrows():
    icon = folium.features.CustomIcon(icon_url, icon_size=(20, 28))  # Creating a custom Icon
    vtb_point = folium.Marker(location=[df_vtb_bk.loc[i,'LAT'], df_vtb_bk.loc[i,'LON']],  # координаты маркера
                                      tooltip=df_vtb_bk.loc[i,'PLACE'],  # всплывающая подсказка
                                      icon=icon,
                                      popup=df_vtb_bk.loc[i,'VIDOP']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    vtb_point.add_to(layer_vtb)
layer_vtb.add_to(m)

#*****************************************************************************************

#******************************** СЛОЙ С бонкоматами sber ************************************

icon_url = '/Users/ruslan/PycharmProjects/maps/img/sber_web_logo.png'
#layer_sber = MarkerCluster(name='Sberbank', show=False)
layer_sber = folium.FeatureGroup(name='Sberbank', show=False)

for i, r in df_sber_bk.iterrows():
    icon = folium.features.CustomIcon(icon_url, icon_size=(20, 28))  # Creating a custom Icon
    sber_point = folium.Marker(location=[df_sber_bk.loc[i,'LAT'], df_sber_bk.loc[i,'LON']],  # координаты маркера
                                      tooltip=df_sber_bk.loc[i,'PLACE'],  # всплывающая подсказка
                                      icon=icon,
                                      popup=df_sber_bk.loc[i,'VIDOP']  # подпись по клику
                                      )
    # sber_point = folium.CircleMarker(location=[df_sber_bk.loc[i,'LAT'], df_sber_bk.loc[i,'LON']],  # координаты маркера
    #                                 tooltip=df_sber_bk.loc[i,'PLACE'],  # всплывающая подсказка
    #                                 popup=df_sber_bk.loc[i, 'VIDOP'],  # подпись по клику
    #                                 radius=5, fill_color='green', color='gray', fill_opacity=0.9)
    # добавляем объект маркер на слой
    sber_point.add_to(layer_sber)
layer_sber.add_to(m)


#*****************************************************************************************


m.keep_in_front(layer_L2,layer_L3,layer_L4)
controlLayers = folium.LayerControl(autoZIndex=False, name = 'test')
controlLayers.add_to(m)

#отображаем карту
m.save('results/map.html')
webbrowser.open('/results/map.html')
