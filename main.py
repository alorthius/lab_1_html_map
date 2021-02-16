import folium

from math import sqrt, sin, cos, asin
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable


def read_file(path: str, users_year: int) -> dict:
    """
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
    latitude_1, longitude_1 = tuple_1
    latitude_2, longitude_2 = tuple_2
    radius = 6371

    def haversin(x: float) -> float:
        return (1 - cos(x)) / 2

    value_to_sqrt_root = haversin(latitude_2 - latitude_1) + cos(latitude_1) * \
                         cos(latitude_2) * haversin(longitude_2 - longitude_1)

    distance = 2 * radius * asin(sqrt(value_to_sqrt_root))
    return distance


def find_coordinates(films_dict: dict, users_coordinates: tuple) -> dict:

    coordinates_dict = {}

    for film_title, all_addresses in films_dict.items():
        for film_address in all_addresses:
            location = geolocator.geocode(film_address)
            try:
                latitude, longitude = location.latitude, location.longitude
            except AttributeError:
                continue

            distance = find_distance_between_two_points(
                users_coordinates, (latitude, longitude))
            dict_key = (latitude, longitude, distance)

            try:
                coordinates_dict[dict_key].add(film_title)
            except KeyError:
                coordinates_dict[dict_key] = {film_title}

    return coordinates_dict


def sort_dict_keys(coordinates_dict: dict) -> list:
    keys_list = sorted(list(coordinates_dict.keys()), key=lambda x: x[2])
    return keys_list[:10]


def create_map(coordinates_dict: dict, keys_list: list, users_coordinates: tuple):
    map = folium.Map(location=[users_coordinates[0], users_coordinates[1]],
                     zoom_start=2)
    fg = folium.FeatureGroup(name="My map")
    for tup in keys_list:
        fg.add_child(folium.Marker(location=[tup[0], tup[1]],
                                   popup=coordinates_dict[tup],
                                   icon=folium.Icon()))
    map.add_child(fg)
    map.save('Map_5.html')


def main_func(path: str, users_year: int, users_coordinates: tuple):
    films_dict = read_file(path, users_year)
    coordinates_dict = find_coordinates(films_dict, users_coordinates)
    keys_list = sorted(list(coordinates_dict.keys()), key=lambda x: x[2])
    keys_list = keys_list[:11]
    create_map(coordinates_dict, keys_list, users_coordinates)


if __name__ == "__main__":
    geolocator = Nominatim(user_agent="my")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.5)
    test_path = 'D:\\Documents\\Projects_Python\\2_semester\\lab_2\\task_2_html_map\\test1.txt'
    path_2 = 'D:\\Documents\\Projects_Python\\2_semester\\lab_2\\task_2_html_map\\test2.txt'
    users_coordinates = (50.4216283, 15.7870889)
    users_year = 2010
    main_func(path_2, users_year, users_coordinates)
