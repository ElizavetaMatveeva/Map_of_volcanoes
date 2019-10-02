import folium
import pandas

# Creating a basic map
map = folium.Map(location = [32, -96], zoom_start = 4, tiles = "Stamen Terrain")

# Creating feature group for volcanoes so all the volcano markers are on the same map layer
fgv = folium.FeatureGroup(name = "Volcanoes")

# Reading the file with information about volcanoes in the US
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

# Defining color of a marker based on elevation of a volcano
def get_color(elevation):
    if elevation < 1000:
        return 'green'
    elif 3000 > elevation >= 1000:
        return 'orange'
    else:
        return 'red'

# Putting markers on the map
for lt, ln, el, nm in zip(lat, lon, elev, name):
    fgv.add_child(folium.Marker(location=[lt, ln], popup = nm + "\n" + str(el) + "m",
                                icon=folium.Icon(color = get_color(el))))

# Creating another feature group for population
fgp = folium.FeatureGroup(name = "Population")

# Creating a layer with international borders and coloring countries according to their population
# (green, orange, or red depending on the amount of people that live there)
fgp.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(),
                            style_function = lambda x: {'fillColor' : 'green' if x['properties']['POP2005'] < 10000000
                            else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

# Adding feature groups to the map, adding layer control panel and saving the result
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map.html")