"""
GitHub link: https://github.com/alorthius/lab_1_html_map
"""
import folium

from math import sqrt, sin, cos, asin, radians

from folium.plugins import MarkerCluster

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable


def read_file(path: str, users_year: int) -> dict:
    """
    Read file "locations.list" by its path. Search by lines for films,
    if it was released in the same year with users_year, find the city
    where it was filmed and create the dictionary, containing film
    title as a key and location as value. Return that dictionary.
    """
    films_dict = {}

    with open(path, 'r', encoding='ISO-8859-1') as file:
        for line in file:
            line = line.strip()

            try:
                title, location = find_info_in_row(line, users_year)
            except TypeError:
                continue

            try:
                films_dict[title].add(location)
            except KeyError:
                films_dict[title] = {location}

    return films_dict


def find_info_in_row(line: str, users_year: int) -> tuple:
    """
    Find film title, its release year and location. If release year
    equalls users_year, that return a tuple with its title and location.
    If the year is not the same or unknown, return None. If line consists
    unknown symbols ('¿½'), return None too.

    >>> find_info_in_row('"#ATown" (2010)		Mount Bonnell, Austin, Texas, USA', 2010)
    ('#ATown', 'Austin, Texas, USA')
    >>> find_info_in_row('"#ATown" (2020)		Mount Bonnell, Austin, Texas, USA', 2010)

    >>> find_info_in_row('"#ATown" (2010)	Mount Bonnell, Austin, Texas, USA (studio)', 2010)
    ('#ATown', 'Austin, Texas, USA')
    >>> find_info_in_row('"#ATown" (2010)	Mount Bonnell, Austin, Federal District, USA', 2010)
    ('#ATown', 'Austin, USA')
    """
    if '¿½' in line:
        return None

    title_ending = line.find('(')
    film_title = line[:title_ending - 1]
    film_title = film_title.replace('"', '')

    try:
        film_year = int(line[title_ending + 1: title_ending + 5])
    except ValueError:
        return None

    if film_year != users_year:
        return None

    line = line.replace('\t', '')
    series_ending = line.find('}')

    if series_ending == -1:
        series_ending = line.find(')')
    film_location = line[series_ending + 1:]
    film_location = film_location.replace(' (TV)', '')
    film_location = film_location.replace(' (studio)', '')

    try:
        *_, city, state, country = film_location.split(', ')
        index = country.find('(')
        if index != -1:
            country = country[:index]
            country = country.strip()

        if 'Federal' in state:
            final_location = city + ', ' + country
        else:
            final_location = city + ', ' + state + ', ' + country

    except ValueError:
        index = film_location.find('(')
        if index != -1:
            film_location = film_location[:index]
            film_location = film_location.strip()
        final_location = film_location

    return film_title, final_location


def find_distance_between_two_points(tuple_1: tuple, tuple_2: tuple) -> float:
    """
    Find distance between two points, using haversine formula.
    Tuples tuple_1 and tuple_2 contains latitude and longitude
    in degrees. Find the distance between them in kilometers
    and return it as a float.

    >>> find_distance_between_two_points((10.10, 15.20), (11.20, 15.30))
    122.80160127206275
    >>> find_distance_between_two_points((50.4216283, 38.7870889), (15.5177729, 38.7870889))
    3881.1316408152866
    """

    def haversin(x: float) -> float:
        """
        Find haversin value of argument x.
        """
        return (1 - cos(x)) / 2

    latitude_1, longitude_1 = tuple_1
    latitude_2, longitude_2 = tuple_2
    # convert to the radians
    longitude_1, latitude_1, longitude_2, latitude_2 = map(
        radians, [longitude_1, latitude_1, longitude_2, latitude_2])
    radius = 6371  # earth radius in kilometers

    value_to_sqrt_root = haversin(latitude_2 - latitude_1) + cos(latitude_1) * \
        cos(latitude_2) * haversin(longitude_2 - longitude_1)

    return 2 * radius * asin(sqrt(value_to_sqrt_root))


def find_coordinates(films_dict: dict, users_coordinates: tuple) -> dict:
    """
    Find each film location in films_dict and find its latitude and longitude.
    Find distance from that location to the one, specified by the coordinates
    users_coordinates. Create new dictionary, where a key is a tuple of two
    coordinates of film location and a distance (e.g. (lat, lon, distance)),
    and the films titles are the values. Return that dictionary.

    >>> (find_coordinates({'Film 1': {'Austin, Texas, USA', \
                                     'Los Angeles, California, USA'}, \
                          'Film 2': {'Los Angeles, California, USA'}}, \
                          (39.966439, -75.040996))) == \
    ({(34.0536909, -118.242766, 3853.757685861244): {'Film 2', 'Film 1'},\
    (30.2711286, -97.7436995, 2319.9128068006653): {'Film 1'}})
    True
    """
    coordinates_dict = {}

    for film_title, all_addresses in films_dict.items():
        for film_address in all_addresses:

            try:
                location = geolocator.geocode(film_address)
                latitude, longitude = location.latitude, location.longitude
            except (AttributeError, GeocoderUnavailable):
                continue

            distance = find_distance_between_two_points(
                users_coordinates, (latitude, longitude))
            dict_key = (latitude, longitude, distance)

            try:
                coordinates_dict[dict_key].add(film_title)
            except KeyError:
                coordinates_dict[dict_key] = {film_title}

    return coordinates_dict


def create_map(coordinates_dict: dict, keys_list: list, users_coordinates: tuple):
    """
    Create map and put markers on the locations where films where located.
    """
    map = folium.Map(location=[users_coordinates[0], users_coordinates[1]],
                     zoom_start=2)

    fg = folium.FeatureGroup(name="My map")
    fg.add_child(folium.Marker(location=[users_coordinates[0], users_coordinates[1]],
                               popup='Here are you!',
                               icon=folium.Icon(color='darkred', icon='flag')))

    films_loc = MarkerCluster(name='films locations').add_to(map)

    for tup in keys_list:
        folium.Marker(location=[tup[0], tup[1]],
                      popup=str(coordinates_dict[tup])[2:-2],
                      icon=folium.Icon(color='darkpurple', icon='film')).add_to(films_loc)
    map.add_child(fg)

    fg_pp = folium.FeatureGroup(name="Countries population")
    fg_pp.add_child(folium.GeoJson(data=open('D:\\Documents\\Projects_Python\\2_semester\\lab_2\\task_2_html_map\\world.json', 'r', encoding='utf-8-sig').read(),
                                   style_function=lambda x:
                                   {'fillColor': 'red' if x['properties']['POP2005'] < 10000000
                                    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                    else 'green' if 20000000 <= x['properties']['POP2005'] < 50000000
                                    else 'blue',
                                    'fillOpacity': 0.1}))
    map.add_child(fg_pp)

    map.add_child(fg_pp)
    map.add_child(folium.LayerControl())

    map.save('Your_map_here.html')
    print('Finished. Check file Your_map_here.html')


def main_func(path: str, users_year: int, users_coordinates: tuple):
    """
    Find 10 different locations on the map, the nearest to the 
    """
    films_dict = read_file(path, users_year)
    coordinates_dict = find_coordinates(films_dict, users_coordinates)
    keys_list = sorted(list(coordinates_dict.keys()), key=lambda x: x[2])
    keys_list = keys_list[:10]
    create_map(coordinates_dict, keys_list, users_coordinates)


if __name__ == "__main__":
    geolocator = Nominatim(user_agent="my")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.5)

    path = str(input('Type path to the file locations.list: '))
    users_year = int(input('Type the year of film release: '))
    latitude = float(input('Type the latitude coordinate as float (e.x. 50.4216283): '))
    longitude = float(input('Type the longitude coordinate as float (e.x. 38.7870889): '))
    users_coordinates = (latitude, longitude)

    main_func(path, users_year, users_coordinates)
