main_path = 'D:\\Documents\\Projects_Python\\2_semester\\lab_2\\task_2_html_map\\locations.list'
test_path = 'D:\\Documents\\Projects_Python\\2_semester\\lab_2\\task_2_html_map\\test1.txt'


latitude = 49.83826
longitude = 24.02324

def read_file(path: str, users_year: int) -> dict:
    """
    """
    films_dict = {}

    with open(path, 'r', encoding='UTF-8', errors='ignore') as file:
        for line in file:
            line = line.strip()
            
            title_ending = line.find(' (')
            film_title = line[:title_ending]
            film_title = film_title.replace('"', '')
            try:
                film_year = int(line[title_ending + 2 : title_ending + 6])
            except ValueError:
                continue
            
            if film_year != users_year:
                continue

            line = line.replace('\t', '')
            series_ending = line.find('}')

            if series_ending == -1:
                series_ending = line.find(')')
            film_location = line[series_ending + 1 :]

            try:
                films_dict[film_title].add(film_location)
            except KeyError:
                films_dict[film_title] = {film_location}
    
    return films_dict
            
print(read_file(main_path, 1966))

