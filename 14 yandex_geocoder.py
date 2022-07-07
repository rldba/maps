# https://yandex.ru/dev/maps/geocoder/
# https://developer.tech.yandex.ru/services/

import os
from yandex_geocoder import Client
import folium
import webbrowser

yandex_geo_api_key = os.environ.get("YandexGeoApiKey")
lat,lon = 0.0, 0.0
# adress = "Уфа Театральная 3"
# adress = "115035, МОСКВА 35, УЛ БАЛЧУГ, 2"
# adress = "Екат Циолковского 18"
adress = "Белорецк Сорока Павших 15А"

client = Client(yandex_geo_api_key)
coordinates = client.coordinates(adress)
lon, lat = coordinates

# создаем карту
m = folium.Map(location=[lat,lon], zoom_start=17, tiles='OpenStreetMap')
#создаем объект маркера
capital_m = folium.Marker(location = [lat,lon],        #координаты маркера
                            tooltip = adress  #всплывающая подсказка
                            )
#добавляем объект маркер на карту
capital_m.add_to(m)

#отображаем карту
m.save('results/map.html')
webbrowser.open('/results/map.html')



