# lab_1_html_map

This module is made to create a html web-map with locations of the films, created in nearby cities. As a result, the user receives a map whith 10 closests locations of films, released in the year indicated by him.

The user enters the year, when he wants films to be found, and his location coordinates - latitude and longitude. The map will consists 10 closests to user's location marks and each of them will show the film title when the mouse is moved over them. If there are a few marks close to each one, they will be replesented as MarkerCluster. Also map provides an additional layer, with 4 types of country population. The country will be filled with *red* color if its population is less than 10 000 000, *orange* if it is in range from 10 000 000 to 20 000 000, *green* if it is in range from 20 000 000 to 50 000 000, and *blue* color with the bigger country population.

- The module works with the file locations.list, whick can be downloaded by [this link](https://drive.google.com/file/d/11KVCDMVb8H0vKzb8bx7VvqOlBUxUfL6x/view?usp=sharing), but there is also its smaller version [test2.txt](https://github.com/alorthius/lab_1_html_map/blob/main/test2.txt) - a chunk of the main database in order to make the programm work faster. Also, it uses side libraries, such as *geopy* and *folium*. Check [requirements.txt](https://github.com/alorthius/lab_1_html_map/blob/main/requirements.txt) for all the requirements.

## Module run example:
```
Type the year of film release: 2010
Type the latitude coordinate as float (e.x. 50.4216283): 50.3
Type the longitude coordinate as float (e.x. 38.7870889): 40.1
```
The final output map (created on a smaller database [test2.txt](https://github.com/alorthius/lab_1_html_map/blob/main/test2.txt)):

![image](https://user-images.githubusercontent.com/73172589/108108684-9d855400-7099-11eb-8679-7c639d6e1158.png)

## HTML document structure:

The row `<!DOCTYPE html>` states that this document is an HTML one.
The `<head>` element contains other elements and scripts, that are not visible for user (except for `<title>`).
The `<title>` element specifies a title for the document.
The `<body>` element is a container for all the visible contents of the document.
`<meta>` defines metatages that are used to store the information for browser.
`<style>` defines style of the elements of the document.
`<script>` describes the scripts, can also contains link to the programm or the programm itself.
`<link>` allows the authors to link their document to other resources.
