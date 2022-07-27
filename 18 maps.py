import geopandas as gpd
import pandas as pd
import folium
import webbrowser
from folium.plugins import MarkerCluster
from folium.plugins import Fullscreen
from folium.plugins import LocateControl

pd.set_option('display.max_columns', None)

#Свердловская обл общая граница
gpd_svd_L1 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl4.shp', encoding='utf-8')
# районы и округа 73 шт 65763000
gpd_svd_L2 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl6.shp', encoding='utf-8')
#print(gpd_svd_L2.loc[gpd_svd_L2['NAME'] == 'Режевской городской округ'])
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

#******************************** читаем эксель с данными ************************************
df_rezh = pd.read_excel('~/PycharmProjects/maps/DataSets/svd/rezh_geo.xlsx')
df_rezh_pko = df_rezh.loc[df_rezh['TYPE'] == 'PKO']             # подразделения КО, включая ППКО
df_rezh_uto = df_rezh.loc[df_rezh['TYPE'] == 'UTO']             # удаленные точки банковского обслуживания
df_rezh_bk = df_rezh.loc[df_rezh['TYPE'] == 'BK']               # банкоматы (вкл выдачу наличных) с исп. ПК
df_rezh_bk_ = df_rezh.loc[df_rezh['TYPE'] == 'BK_']             # банкоматы без исп. ПК
df_rezh_post = df_rezh.loc[df_rezh['TYPE'] == 'RUSSIA_POST']    # отделения АО "Почта России"
df_rezh_cash = df_rezh.loc[df_rezh['TYPE'] == 'CASH_OUT']       # выдача наличных с POS-терминала
df_rezh_pay = df_rezh.loc[df_rezh['TYPE'] == 'PAY_POINT']       # точки, предоставляющие возможность оплаты наличными деньгами
df_rezh_mfo = df_rezh.loc[df_rezh['TYPE'] == 'MFO']             # подразделения микрофинансовых организаций
df_rezh_ins = df_rezh.loc[df_rezh['TYPE'] == 'INS']             # подразделения субъектов страхового дела

#создаю карту
m = folium.Map(location=[57.373777, 61.391648], zoom_start=10, tiles='OpenStreetMap')
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

gpd_l2_current = gpd_svd_L2.loc[gpd_svd_L2['NAME'] == 'Режевской городской округ']
sim_geo = gpd.GeoSeries(gpd_l2_current.iloc[0]['geometry']).simplify(tolerance=0.001)
geo_j = sim_geo.to_json()
geo_j = folium.GeoJson(data=geo_j,
                       style_function=lambda x: {'fillColor': '#00000000', 'color': 'green',
                                                 'weight': 4})  # 'fillColor': 'orange',
geo_j_info = '<b>' + str(gpd_l2_current.iloc[0]['NAME']) + '</b>'
folium.Tooltip(geo_j_info).add_to(geo_j)  # подсказки всплывающие при наведении мыши
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

# https://fontawesome.com/v4/icons/
# {'darkpurple', 'darkgreen', 'darkblue', 'green', 'darkred', 'blue', 'white', 'black', 'pink', 'gray', 'cadetblue', 'beige', 'lightred', 'orange', 'red', 'purple', 'lightblue', 'lightgreen', 'lightgray'}.

#******************************** СЛОЙ С PKO ************************************
icon_url = '/Users/ruslan/PycharmProjects/maps/img/alfabank_web_logo.png'
#layer_alfa = MarkerCluster(name='Alfa Bank', show=False)
layer_pko = folium.FeatureGroup(name='Подразделения КО, включая ППКО', show = False)

for i, r in df_rezh_pko.iterrows():
    icon = folium.Icon(icon="home", color="green", prefix='fa')
    point = folium.Marker(location=[df_rezh_pko.loc[i,'LAT'], df_rezh_pko.loc[i,'LON']],  # координаты маркера
                                      tooltip=df_rezh_pko.loc[i,'NAME'],  # всплывающая подсказка
                                      icon=icon,
                                      # popup=df_rezh_pko.loc[i,'VIDOP']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    point.add_to(layer_pko)
layer_pko.add_to(m)
#*****************************************************************************************

#******************************** СЛОЙ С UTO ************************************
icon_url = '/Users/ruslan/PycharmProjects/maps/img/alfabank_web_logo.png'
#layer_alfa = MarkerCluster(name='Alfa Bank', show=False)
layer_uto = folium.FeatureGroup(name='Удаленные точки банковского обслуживания', show = False)

for i, r in df_rezh_uto.iterrows():
    icon = folium.Icon(icon="home", color="cadetblue", prefix='fa')
    point = folium.Marker(location=[df_rezh_uto.loc[i,'LAT'], df_rezh_uto.loc[i,'LON']],  # координаты маркера
                                      tooltip=df_rezh_uto.loc[i,'NAME'],  # всплывающая подсказка
                                      icon=icon,
                                      # popup=df_rezh_pko.loc[i,'VIDOP']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    point.add_to(layer_uto)
layer_uto.add_to(m)
#*****************************************************************************************

#******************************** СЛОЙ С BK ************************************
icon_url = '/Users/ruslan/PycharmProjects/maps/img/alfabank_web_logo.png'
#layer_alfa = MarkerCluster(name='Alfa Bank', show=False)
layer_bk = folium.FeatureGroup(name='Банкоматы (вкл. выдачу наличных) с исп. платежных карт', show = False)

for i, r in df_rezh_bk.iterrows():
    icon = folium.Icon(icon="credit-card", color="green", prefix='fa')
    point = folium.Marker(location=[df_rezh_bk.loc[i,'LAT'], df_rezh_bk.loc[i,'LON']],  # координаты маркера
                                      tooltip=df_rezh_bk.loc[i,'NAME'],  # всплывающая подсказка
                                      icon=icon,
                                      popup=df_rezh_bk.loc[i,'BK_DESC']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    point.add_to(layer_bk)
layer_bk.add_to(m)
#*****************************************************************************************

#******************************** СЛОЙ С BK_ ************************************
icon_url = '/Users/ruslan/PycharmProjects/maps/img/alfabank_web_logo.png'
#layer_alfa = MarkerCluster(name='Alfa Bank', show=False)
layer_bk_ = folium.FeatureGroup(name='Банкоматы без исп. платежных карт', show = False)

for i, r in df_rezh_bk_.iterrows():
    icon = folium.Icon(icon="credit-card", color="cadetblue", prefix='fa')
    point = folium.Marker(location=[df_rezh_bk_.loc[i,'LAT'], df_rezh_bk_.loc[i,'LON']],  # координаты маркера
                                      tooltip=df_rezh_bk_.loc[i,'NAME'],  # всплывающая подсказка
                                      icon=icon,
                                      popup=df_rezh_bk_.loc[i,'BK_DESC']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    point.add_to(layer_bk_)
layer_bk_.add_to(m)
#*****************************************************************************************

#******************************** СЛОЙ С POST ************************************
#layer_alfa = MarkerCluster(name='Alfa Bank', show=False)
layer_post = folium.FeatureGroup(name='Отделения АО "Почта России"', show = False)

for i, r in df_rezh_post.iterrows():
    icon=folium.Icon(icon="fa-solid fa-envelope", color="blue", prefix='fa')
    point = folium.Marker(location=[df_rezh_post.loc[i,'LAT'], df_rezh_post.loc[i,'LON']],  # координаты маркера
                                      tooltip=df_rezh_post.loc[i,'NAME'],  # всплывающая подсказка
                                      icon=icon,
                                      # popup=df_rezh_post.loc[i,'BK_DESC']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    point.add_to(layer_post)
layer_post.add_to(m)
#*****************************************************************************************

#******************************** СЛОЙ С POS ************************************

layer_cash = folium.FeatureGroup(name='Выдача наличных с POS-терминала', show = False)

for i, r in df_rezh_cash.iterrows():
    icon=folium.Icon(icon="fa-rub", color="green", prefix='fa')
    point = folium.Marker(location=[r['LAT'], r['LON']],  # координаты маркера
                                      tooltip=f"Выдача наличных с POS-терминала ({r['NAME']})",  # всплывающая подсказка
                                      icon=icon,
                                      # popup=df_rezh_post.loc[i,'BK_DESC']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    point.add_to(layer_cash)
layer_cash.add_to(m)
#*****************************************************************************************

#******************************** СЛОЙ С PAY ************************************

layer_pay = folium.FeatureGroup(name='Точки, предоставляющие возможность оплаты наличными деньгами', show = False)

for i, r in df_rezh_pay.iterrows():
    icon=folium.Icon(icon="fa-rub", color="blue", prefix='fa')
    point = folium.Marker(location=[r['LAT'], r['LON']],  # координаты маркера
                                      tooltip=f"Оплата наличными деньгами ({r['NAME']})",  # всплывающая подсказка
                                      icon=icon,
                                      # popup=df_rezh_post.loc[i,'BK_DESC']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    point.add_to(layer_pay)
layer_pay.add_to(m)
#*****************************************************************************************

#******************************** СЛОЙ С MFO ************************************

layer_mfo = folium.FeatureGroup(name='Подразделения МФО', show = False)

for i, r in df_rezh_mfo.iterrows():
    icon=folium.Icon(icon="fa-percent", color="darkred", prefix='fa')
    point = folium.Marker(location=[r['LAT'], r['LON']],  # координаты маркера
                                      tooltip=f"{r['NAME']}",  # всплывающая подсказка
                                      icon=icon,
                                      # popup=df_rezh_post.loc[i,'BK_DESC']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    point.add_to(layer_mfo)
layer_mfo.add_to(m)
#*****************************************************************************************

#******************************** СЛОЙ С INS ************************************

layer_ins = folium.FeatureGroup(name='Подразделения субъектов страхового дела', show = False)

for i, r in df_rezh_ins.iterrows():
    icon=folium.Icon(icon="fa-wheelchair-alt", color="red", prefix='fa')
    point = folium.Marker(location=[r['LAT'], r['LON']],  # координаты маркера
                                      tooltip=f"{r['NAME']}",  # всплывающая подсказка
                                      icon=icon,
                                      # popup=df_rezh_post.loc[i,'BK_DESC']  # подпись по клику
                                      )
            # добавляем объект маркер на карту
    point.add_to(layer_ins)
layer_ins.add_to(m)
#*****************************************************************************************


m.keep_in_front(layer_L2,layer_L3)
controlLayers = folium.LayerControl(autoZIndex=False, name = 'test')
controlLayers.add_to(m)

Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
).add_to(m)

LocateControl(position="topright").add_to(m)

#отображаем карту
m.save('results/map.html')
webbrowser.open('/results/map.html')

