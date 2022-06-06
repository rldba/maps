import folium
import webbrowser

#создаю карту
m = folium.Map(location=[56.838924, 60.605701], zoom_start=5, tiles='OpenStreetMap')
#создаю маркеры всех столиц регионов Уральского ГУ
capital_m = folium.Marker(location = [56.838924, 60.605701],popup = 'Екатеринбург', tooltip = 'Уральское ГУ Банка России')
capital_m.add_to(m)
capital_m = folium.Marker(location = [58.029682, 56.266792],popup = 'Пермь')
capital_m.add_to(m)
capital_m = folium.Marker(location = [57.156727, 65.542508],popup = 'Тюмень')
capital_m.add_to(m)
capital_m = folium.Marker(location = [55.456180, 65.322805],popup = 'Курган')
capital_m.add_to(m)
capital_m = folium.Marker(location = [51.768955, 55.096627],popup = 'Оренбург')
capital_m.add_to(m)
capital_m = folium.Marker(location = [55.163769, 61.399334],popup = 'Челябинск')
capital_m.add_to(m)
capital_m = folium.Marker(location = [54.771648, 56.026932],popup = 'Уфа')
capital_m.add_to(m)

#отображаем карту
m.save('results/map.html')
webbrowser.open('/results/map.html')
