import geopandas as gpd
import pandas as pd
import folium
import webbrowser
from folium.plugins import MarkerCluster
pd.set_option('display.max_columns', None)

# Границы территориальных образование России
gpd_russia = gpd.read_file('~/PycharmProjects/maps/GeoData/ru/gadm36_RUS_1.shp', encoding='utf-8')

#******************************** Верификация / очистка / загруженых данных ************************************

#******************************** читаем эксель с данными по структурным подразделениям Банка России ************************************
df_cbr_str = pd.read_excel('~/PycharmProjects/maps/DataSets/cbr_str_geo.xlsx')
df_cbr_str.reset_index(drop=True, inplace=True)

#создаю карту
m = folium.Map(location=[62.867151, 93.290412], zoom_start=4, tiles='OpenStreetMap')
folium.TileLayer('CartoDB positron').add_to(m)
folium.TileLayer('CartoDB dark_matter').add_to(m)

#******************************** СЛОЙ С ГРАНИЦАМИ РАЙОНОВ И ОКРУГОВ С ПОДПИСЯМИ ************************************
layer_russia = folium.FeatureGroup(name='Границы территориальных образование России')

for _, r in gpd_russia.iterrows():
    # Без упрощения представления каждого района карта может не отображаться
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j,
                           style_function=lambda x: {'fillColor': '#00000000', 'color': 'orange', 'weight': 3}) #'fillColor': 'orange',
    geo_j_info =  '<b>' + str(r['NL_NAME_1']) + '</b>'
    folium.Tooltip(geo_j_info).add_to(geo_j) # подсказки всплывающие при наведении мыши
    layer_russia.add_child(geo_j)

layer_russia.add_to(m)
#*****************************************************************************************

#******************************** СЛОЙ С бонкоматами Alfa ************************************

layer_tu = folium.FeatureGroup(name='ТУ Банка России', show = False)

for i, r in df_cbr_str.iterrows():

    # if r['LEVEL'] == 1:
    #     icon_url = '/Users/ruslan/PycharmProjects/maps/img/cbr_lvl1_.png'
    # elif r['LEVEL'] == 2:
    #     icon_url = '/Users/ruslan/PycharmProjects/maps/img/cbr_lvl2_.png'
    # else:
    #     icon_url = '/Users/ruslan/PycharmProjects/maps/img/cbr_lvl3_.png'
    #
    # icon = folium.features.CustomIcon(icon_url, icon_size=(25, 40))  # Creating a custom Icon

    if r['LEVEL'] == 1:
        icon = folium.Icon(color="red")
    elif r['LEVEL'] == 2:
        icon = folium.Icon(color="green")
    else:
        icon = folium.Icon(color="blue")

    tu_point = folium.Marker(location=[r['LAT'], r['LON']],  # координаты маркера
                                      tooltip=r['NAIM'],  # всплывающая подсказка
                                      icon=icon,
                                      popup=df_cbr_str.loc[i,'ADRESS']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    tu_point.add_to(layer_tu)
layer_tu.add_to(m)

#*****************************************************************************************

m.keep_in_front(layer_tu,layer_russia)
controlLayers = folium.LayerControl(autoZIndex=False, name = 'test')
controlLayers.add_to(m)
#
#отображаем карту
m.save('results/map.html')
webbrowser.open('/results/map.html')