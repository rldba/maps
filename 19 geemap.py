import ee
import geemap

Map = geemap.Map(toolbar_ctrl=True, layer_ctrl=True)
Map.add_basemap('HYBRID')
Map.add_basemap('ROADMAP')
Map.to_html(filename='/results/geemap.html', title='My Map', width='100%', height='880px')