import geopandas as gpd
import pandas as pd
import folium
import webbrowser
from folium.plugins import Fullscreen
from folium.plugins import LocateControl
from branca.element import Template, MacroElement

pd.set_option('display.max_columns', None)

template_caption = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<body>
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:0px; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:25px; left: 10px; top: 10px;'>

<div class='legend-title'>Карта доступности платежных услуг</div>
<div class='legend-scale'><font size="3">Ржевский городской округ Свердловской обл.</font></div>
</div>
</body>
</html>

{% endmacro %}"""

template_legend = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<body>
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; left: 10px; top: 120px;'>
<div class='legend-title'> </div>
<div class='legend-scale'>
  <dl class='legend-labels'>
    <dt><img src="/img/pay_point.png" width="20" height="20"> точки, предоставляющие возможность оплаты наличными деньгами</dt>
    <dt><img src="/img/pko.png" width="20" height="20"> подразделения КО, включая ППКО</dt>
    <dt><img src="/img/uto.png" width="20" height="20"> удаленные точки банковского обслуживания</dt>
    <dt><img src="/img/bk.png" width="20" height="20"> банкоматы (вкл выдачу наличных) с исп. карт</dt>
    <dt><img src="/img/bk_.png" width="20" height="20"> банкоматы без исп. карт</dt>
    <dt><img src="/img/post.png" width="20" height="20"> отделения АО "Почта России"</dt>
    <dt><img src="/img/cash.png" width="20" height="20"> выдача наличных с POS-терминала</dt>
    <dt><img src="/img/mfo.png" width="20" height="20"> подразделения микрофинансовых организаций</dt>
    <dt><img src="/img/ins.png" width="20" height="20"> подразделения субъектов страхового дела</li>    
  </dl>
</div>
</div>
</body>
</html>
{% endmacro %}"""

macro_caption = MacroElement()
macro_caption._template = Template(template_caption)

macro_legend = MacroElement()
macro_legend._template = Template(template_legend)

# Свердловская обл / районы и округа 73 шт 65763000
gpd_svd_L2 = gpd.read_file('~/PycharmProjects/maps/GeoData/svd/boundary-polygon-lvl6.shp', encoding='utf-8')

# ******************************** Верификация / очистка / загруженых данных ************************************
gpd_svd_L2.loc[(gpd_svd_L2['NAME'] == 'Камышловский район'), 'oktmo'] = 65623000
gpd_svd_L2['oktmo'] = pd.to_numeric(gpd_svd_L2['oktmo'])
gpd_svd_L2['oktmo'] = gpd_svd_L2['oktmo'] / 1000
gpd_svd_L2['oktmo'] = pd.to_numeric(gpd_svd_L2['oktmo'], downcast='integer')

# ******************************** ОБЪЕДИНЯЕМ ГЕОПАНДЫ В ЕДИНОЕ ПРОСТРАНСТВО ************************************
gpd_L2 = gpd_svd_L2

# ******************************** читаем эксель с данными ************************************
df_rezh = pd.read_excel('~/PycharmProjects/maps/DataSets/svd/rezh_geo.xlsx')
# df_rezh_pko = df_rezh.loc[df_rezh['TYPE'] == 'PKO']             # подразделения КО, включая ППКО
# df_rezh_uto = df_rezh.loc[df_rezh['TYPE'] == 'UTO']             # удаленные точки банковского обслуживания
# df_rezh_bk = df_rezh.loc[df_rezh['TYPE'] == 'BK']               # банкоматы (вкл выдачу наличных) с исп. ПК
# df_rezh_bk_ = df_rezh.loc[df_rezh['TYPE'] == 'BK_']             # банкоматы без исп. ПК
# df_rezh_post = df_rezh.loc[df_rezh['TYPE'] == 'RUSSIA_POST']    #отделения АО "Почта России"
# df_rezh_cash = df_rezh.loc[df_rezh['TYPE'] == 'CASH_OUT']       # выдача наличных с POS-терминала
# df_rezh_pay = df_rezh.loc[df_rezh['TYPE'] == 'PAY_POINT']       # точки, предоставляющие возможность оплаты наличными деньгами
# df_rezh_mfo = df_rezh.loc[df_rezh['TYPE'] == 'MFO']             # подразделения микрофинансовых организаций
# df_rezh_ins = df_rezh.loc[df_rezh['TYPE'] == 'INS']             # подразделения субъектов страхового дела

# ******************************** создаю карту
m = folium.Map(location=[57.373777, 61.391648], zoom_start=10, tiles='OpenStreetMap', zoom_control=False)
folium.TileLayer('CartoDB positron').add_to(m)
folium.TileLayer('CartoDB dark_matter').add_to(m)

# ******************************** СЛОЙ с ГРАНИЦей Режевской городской округ ************************************
layer_L2 = folium.FeatureGroup(name='Режевской городской округ')

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
# *****************************************************************************************

#  КАТАЛОГ ИКОНОК ДЛЯ МАРКЕРОВ

# https://fontawesome.com/v4/icons/
# {'darkpurple', 'darkgreen', 'darkblue', 'green', 'darkred', 'blue', 'white', 'black', 'pink', 'gray', 'cadetblue', 'beige', 'lightred', 'orange', 'red', 'purple', 'lightblue', 'lightgreen', 'lightgray'}.

# ******************************** СЛОЙ С МАРКЕРАМИ ************************************

# icon = folium.Icon(icon="home", color="green", prefix='fa') #PKO
# icon = folium.Icon(icon="home", color="cadetblue", prefix='fa') #UTO
# icon=folium.Icon(icon="fa-solid fa-envelope", color="blue", prefix='fa') # POST Office
# icon=folium.Icon(icon="fa-rub", color="green", prefix='fa') # POS - terminals
# icon=folium.Icon(icon="fa-rub", color="blue", prefix='fa') # PAY
# icon=folium.Icon(icon="fa-percent", color="darkred", prefix='fa') # MFO
# icon=folium.Icon(icon="fa-wheelchair-alt", color="red", prefix='fa') # INS

layer_bk = folium.FeatureGroup(name='Банкоматы / нал', show=True)
layer_bk_ = folium.FeatureGroup(name='Банкоматы / безнал', show=True)
layer_pko = folium.FeatureGroup(name='Подразделения КО', show=True)
layer_uto = folium.FeatureGroup(name='Удаленные точки БО', show=True)
layer_mfo = folium.FeatureGroup(name='МФО', show=True)
layer_ins = folium.FeatureGroup(name='Страховые организации', show=True)
layer_pay = folium.FeatureGroup(name='Точки оплаты наличными', show=True)
layer_cash = folium.FeatureGroup(name='Cash out', show=True)
layer_post = folium.FeatureGroup(name='Почта России', show=True)

for i, r in df_rezh.iterrows():
    if r['TYPE'] == 'BK':
        icon = folium.Icon(icon="credit-card", color="green", prefix='fa')
        point = folium.Marker(location=[r['LAT'], r['LON']],tooltip=r['NAME'],icon=icon, popup=r['BK_DESC'])
        point.add_to(layer_bk)
    elif r['TYPE'] == 'BK_':
        icon = folium.Icon(icon="credit-card", color="cadetblue", prefix='fa')
        point = folium.Marker(location=[r['LAT'], r['LON']],tooltip=r['NAME'],icon=icon, popup=r['BK_DESC'])
        point.add_to(layer_bk_)
    elif r['TYPE'] == 'PKO':
        icon = folium.Icon(icon="home", color="green", prefix='fa')
        point = folium.Marker(location=[r['LAT'], r['LON']],tooltip=r['NAME'],icon=icon, popup=r['ADRESS'])
        point.add_to(layer_pko)
    elif r['TYPE'] == 'UTO':
        icon = folium.Icon(icon="home", color="cadetblue", prefix='fa')
        point = folium.Marker(location=[r['LAT'], r['LON']],tooltip=r['NAME'],icon=icon, popup=r['ADRESS'])
        point.add_to(layer_uto)
    elif r['TYPE'] == 'MFO':
        icon = folium.Icon(icon="fa-percent", color="darkred", prefix='fa')
        point = folium.Marker(location=[r['LAT'], r['LON']],tooltip=r['NAME'],icon=icon, popup=r['ADRESS'])
        point.add_to(layer_mfo)
    elif r['TYPE'] == 'INS':
        icon = folium.Icon(icon="fa-wheelchair-alt", color="red", prefix='fa')
        point = folium.Marker(location=[r['LAT'], r['LON']],tooltip=r['NAME'],icon=icon, popup=r['ADRESS'])
        point.add_to(layer_ins)
    elif r['TYPE'] == 'PAY_POINT':
        icon = folium.Icon(icon="fa-rub", color="blue", prefix='fa')
        point = folium.Marker(location=[r['LAT'], r['LON']],tooltip=r['NAME'],icon=icon, popup=r['BK_DESC'])
        point.add_to(layer_pay)
    elif r['TYPE'] == 'CASH_OUT':
        icon = folium.Icon(icon="fa-rub", color="green", prefix='fa')
        point = folium.Marker(location=[r['LAT'], r['LON']],tooltip=r['NAME'],icon=icon, popup=r['ADRESS'])
        point.add_to(layer_cash)
    elif r['TYPE'] == 'RUSSIA_POST':
        icon = folium.Icon(icon="fa-solid fa-envelope", color="blue", prefix='fa')
        point = folium.Marker(location=[r['LAT'], r['LON']],tooltip=r['NAME'],icon=icon, popup=r['ADRESS'])
        point.add_to(layer_post)
    else:
        icon = folium.Icon(icon="fa-question", color="red", prefix='fa')

    # point = folium.Marker(location=[r['LAT'], r['LON']],  # координаты маркера
    #                       tooltip=r['NAME'],  # всплывающая подсказка
    #                       icon=icon,
    #                       popup=r['TYPE']  # подпись по клику
    #                       )
    # # добавляем объект маркер на карту
    # point.add_to(layer_markers)

layer_bk.add_to(m)
layer_bk_.add_to(m)
layer_pko.add_to(m)
layer_uto.add_to(m)
layer_pay.add_to(m)
layer_mfo.add_to(m)
layer_ins.add_to(m)
layer_cash.add_to(m)
layer_post.add_to(m)

# *****************************************************************************************

# создаем контроллер Fullscreen
Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
).add_to(m)
# создаем контроллер текущего местоположения
LocateControl(position="topright").add_to(m)

# задаем очередность слоев
m.keep_in_front(layer_L2)
# создаем контроллер выборо слоев
controlLayers = folium.LayerControl(autoZIndex=False, collapsed=False)
controlLayers.add_to(m)

# добавляем заголовок и легенду
m.get_root().add_child(macro_caption)
m.get_root().add_child(macro_legend)

# отображаем карту
m.save('results/map.html')
webbrowser.open('/results/map.html')