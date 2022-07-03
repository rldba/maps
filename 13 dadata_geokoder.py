# https://fias.nalog.ru

import os
from dadata import Dadata
import folium
import webbrowser

token = os.environ.get('DADATA_TOKEN')
secret = os.environ.get('DADATA_SECRET')
lat, lon = 0.0, 0.0

# fias = "2389c6ad-0ff1-4ac9-bbd8-51b5ba23bd70" # Уфа Театральная 3
# fias = "2f0206c5-88fc-404b-b2ab-acf20cad50e9" # Екатеринбург Циолковского 18
fias = "249f2b73-1bfb-43d2-9a94-ee27a433efd2" # Первоуральск Огнеупорщиков 17

# adress = "Уфа Театральная 3"
# adress = "Екатеринбург Циолковского 18"
# adress = "Белорецк Сорока Павших 15А"


with Dadata(token, secret) as dadata:
    result = dadata.find_by_id("address", fias)
    lat = result[0]['data']['geo_lat']
    lon = result[0]['data']['geo_lon']

    # result = dadata.clean("address", "Уфа театральная 3")
    # lat = result['geo_lat']
    # lon = result['geo_lon']

# создаем карту
m = folium.Map(location=[lat,lon], zoom_start=17, tiles='OpenStreetMap')
#создаем объект маркера
capital_m = folium.Marker(location = [lat,lon],        #координаты маркера
                            tooltip = fias  #всплывающая подсказка
                            )
#добавляем объект маркер на карту
capital_m.add_to(m)

#отображаем карту
m.save('results/map.html')
webbrowser.open('/results/map.html')
