import folium
import webbrowser

#создаем карту
m = folium.Map(location=[54.771648, 56.026932], zoom_start=10, tiles='OpenStreetMap') #вечная, всем привычная классика

#m = folium.Map(location=[56.838924, 60.605701], zoom_start=9, tiles='CartoDB positron') #выбеленная основа с англорусскими названиями
#m = folium.Map(location=[56.838924, 60.605701], zoom_start=9, tiles='CartoDB dark_matter') #очень темная/ почти черная (ночная) карта
# m = folium.Map(location=[56.838924, 60.605701], zoom_start=9, tiles='Stamen Toner')  #черно-белая (похоже на негатив)
#m = folium.Map(location=[56.838924, 60.605701], zoom_start=9, tiles='Stamen Watercolor') #вода и суша
#m = folium.Map(location=[56.838924, 60.605701], zoom_start=9, tiles='Stamen Terrain') #горы и леса


m.save('results/map.html')
webbrowser.open('/results/map.html')