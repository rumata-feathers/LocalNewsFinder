import csv

from flask import Flask, render_template
import folium
from folium.plugins import MiniMap, MousePosition, MarkerCluster, FastMarkerCluster
import pandas
from gnews import GNews
import pickle

with open('daily_news.pkl', 'rb') as f:
    daily_news = pickle.load(f)
f.close()

app = Flask(__name__)
google_news = GNews()
euro_news = 'https://www.euronews.com/tag/'
independent_news = 'https://www.independent.co.uk/topic/'
formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
cities = pandas.read_csv("worldcities.csv").set_index('city').T.to_dict('list')
countries = set(cities[city][2] for city in cities)


def get_search_pop_up(city):
    e_n = '<a href=' + euro_news + city.lower() + ">Euronews in " + city + '</a>'
    in_n = '<a href=' + independent_news + city.lower() + ">Independent news in " + city + '</a>'
    links = e_n + '\n' + in_n
    return daily_news[city] + links
    # return links


def calculate_countries_cluster(cities_database, countries_database, cluster_map):
    countries_cluster = dict()
    for country in countries_database:
        # countries_cluster[country] = list()
        countries_cluster[country] = MarkerCluster(control=False).add_to(cluster_map)

    for city in cities_database:
        if len(get_search_pop_up(city).split('\n')) == 2:
            continue
        marker = folium.Marker(
            location=[cities_database[city][0], cities_database[city][1]],
            popup=get_search_pop_up(city),
            tooltip=city + ', ' + cities_database[city][2],
            icon=None,
            ).add_to(countries_cluster[cities_database[city][2]])
        # )
        # countries_cluster[cities_database[city][2]].append(marker)
    #
    # for country in countries_database:
    #     countries_cluster[country] = FastMarkerCluster(control=False, data=countries_cluster[country])


@app.route('/')
def index():
    folium_map = folium.Map(zoom_start=8, world_copy_jump=False, no_wrap=True, tiles=None)
    folium_map.add_child(MiniMap(tile_layer=None, toggle_display=True, position='topleft', zoom_level_offset=-6))

    folium.raster_layers.TileLayer(
        tiles="https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png",
        attr="theme",
        name="white_theme",
        max_zoom=12,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
        overlay=False,
        control=True
    ).add_to(folium_map)

    folium.raster_layers.TileLayer(
        tiles="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png",
        attr="theme",
        name="black_theme",
        max_zoom=12,
        subdomains=["mt0", "mt1", "mt2", "mt3"],
        overlay=False,
        control=True,
    ).add_to(folium_map)

    MousePosition(separator=" | ",
                  empty_string="NaN",
                  lng_first=True,
                  num_digits=20,
                  prefix="Coordinates:",
                  lat_formatter=formatter,
                  lng_formatter=formatter).add_to(folium_map)

    calculate_countries_cluster(cities_database=cities, countries_database=countries,
                                cluster_map=folium_map)

    folium.plugins.Geocoder().add_to(folium_map)

    folium.LayerControl().add_to(folium_map)

    folium_map.save('map.html')
    return folium_map._repr_html_()


if __name__ == '__main__':
    index()
    app.run(debug=True)
