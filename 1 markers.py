import folium
import webbrowser

m = folium.Map(location=[56.838924, 60.605701], zoom_start=9, tiles='OpenStreetMap')
folium.TileLayer('CartoDB positron').add_to(m)      #выбеленная основа с англорусскими названиями
folium.TileLayer('CartoDB dark_matter').add_to(m)   #очень темная/ почти черная (ночная) карта
folium.TileLayer('Stamen Toner').add_to(m)          #черно-белая (похоже на негатив)
folium.TileLayer('Stamen Watercolor').add_to(m)     #вода и суша
folium.TileLayer('Stamen Terrain').add_to(m)        #горы и леса

#создаем объект маркера
capital_m = folium.Marker(location = [56.838924, 60.605701],        #координаты маркера
                            tooltip = 'Уральское ГУ Банка России',  #всплывающая подсказка
                            #icon=folium.Icon(icon="cloud"),
                            popup = 'Екатеринбург'                  #подпись по клику
                            )
#кастомизация маркеров
#icon=folium.Icon(icon="cloud")
#icon=folium.Icon(icon="info-sign", color="green")

#добавляем объект маркер на карту
capital_m.add_to(m)

folium.LayerControl(autoZIndex=False).add_to(m)

#отображаем карту
m.save('results/map.html')
webbrowser.open('/results/map.html')

