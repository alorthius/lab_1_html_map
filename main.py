from math import sqrt, sin, cos, asin
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable

geolocator = Nominatim(user_agent="my")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.5)

main_path = 'D:\\Documents\\Projects_Python\\2_semester\\lab_2\\task_2_html_map\\locations.list'
test_path = 'D:\\Documents\\Projects_Python\\2_semester\\lab_2\\task_2_html_map\\test1.txt'
path_2 = 'D:\\Documents\\Projects_Python\\2_semester\\lab_2\\task_2_html_map\\test2.txt'

latitude = 49.83826
longitude = 24.02324


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

        if state == 'Federal District':
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


films_dict = read_file(path_2, 2010)
# print(films_dict)


def find_coordinates(films_dict: dict):

    new_dict = {}

    for film_title, all_addresses in films_dict.items():
        for film_address in all_addresses:
            location = geolocator.geocode(film_address)

            try:
                new_dict[film_title].add((location.latitude, location.longitude))
            except AttributeError:
                    continue

            except KeyError:
                # print(film_title, all_addresses, film_address, location)
                try:
                    new_dict[film_title] = {(location.latitude, location.longitude)}
                except AttributeError:
                    continue

    return new_dict


# new_dict = find_coordinates(films_dict)
# print(new_dict)


def find_distance_between_two_points(tuple_1: tuple, tuple_2: tuple) -> float:
    latitude_1, longitude_1 = tuple_1
    latitude_2, longitude_2 = tuple_2
    r = 6371

    def haversin(x: float) -> float:
        return (1 - cos(x)) / 2

    # h = (sin((latitude_2 - latitude_1) / 2)) ** 2 + cos(latitude_1) * cos(latitude_2) * (sin((longitude_2 - longitude_1) / 2)) ** 2

    h = haversin(latitude_2 - latitude_1) + cos(latitude_1) * cos(latitude_2) * haversin(longitude_2 - longitude_1)
    print(h)
    print(sqrt(h))
    print(asin(sqrt(h)))
    distance = 2 * r * asin(sqrt(h))
    return distance

# print(find_distance_between_two_points((37.5666791, 126.9782914), (41.8933203, 12.4829321)))
print(find_distance_between_two_points((50.4216283, 15.7870889), (50.5571513, 14.8754876)))