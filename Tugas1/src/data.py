from actor import get_actors
from bs4 import BeautifulSoup as bs
import requests
import time
import json


def get_movies(actor):
    """
    get movies with ratings and producer from actor
    :param actor: actor name to get movie
    :return: list of dictionary of movies
    """
    # specify for leonardo di caprio
    if actor == 'Leonardo DiCaprio':
        actor = 'Leonardo Di Caprio'

    # actor name in url
    actor = actor.lower().replace(' ', '_')
    act = actor.replace('-', '_')

    # request
    url = 'https://www.rottentomatoes.com/celebrity/' + act
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers)

    # get html in soup
    soup = bs(response.text, 'html.parser')

    # check whether found
    if soup.find('h1').get_text() == '404 - Not Found':
        act = actor.replace('-', '')

        # request
        url = 'https://www.rottentomatoes.com/celebrity/' + act
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers)

        # get html in soup
        soup = bs(response.text, 'html.parser')

    # table of movies
    movies_table = soup.find('table', id='filmographyTbl').find('tbody').findAll('tr')

    # list of dict of movies
    movies = []

    # take movie data
    for movie in movies_table:
        print('getting movie data...')
        reviewed = movie.find('td').find('span')['class']
        if len(reviewed) == 1:
            mov_data = movie.findAll('td')
            rating = mov_data[0].get_text().replace('\n', '')
            title = mov_data[1].get_text().replace('\n', '')
            print(title)
            year = mov_data[4].get_text().replace('\n', '')
            mov_data = get_movie_data(movie.find('a')['href'])
            movie_dict = {'title': title,
                          'rating': rating,
                          'year': year}
            movie_dict.update(mov_data)
            movies.append(movie_dict)

        time.sleep(0.2)

    print(movies)
    return movies


def get_movie_data(url):
    """
    method to scrape movie data
    :param url: link of movie data
    :return: dictionary of movie data
    """
    # request page
    url = 'https://www.rottentomatoes.com' + url
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers)

    # get html in soup
    soup = bs(response.text, 'html.parser')

    # get movie data
    movie_data = soup.find(class_='content-meta info').findAll('li')
    genre = movie_data[1].findAll('a')
    for i in range(len(genre)):
        genre[i] = genre[i].get_text().strip()
    director = movie_data[2].findAll('div')[1].get_text().strip()
    studio = movie_data[len(movie_data)-1].findAll('div')[1].get_text().strip()
    movie_dict = {'genre': genre,
                  'director': director,
                  'studio': studio}

    return movie_dict


def make_data():
    """
    method to get all data from websites and save it to json file
    """
    # getting actors name
    actors = get_actors()

    data = []
    # iterate actors to find data of actor
    for actor in actors:
        try:
            print(actor)
            movie_dict = {'actor': actor,
                          'movies': get_movies(actor)}
            data.append(movie_dict)
        except:
            continue

        time.sleep(0.25)

    # creating json data
    with open('../data/data.json', 'w') as outfile:
        json.dump(data, outfile)


def main():
    make_data()


if __name__ == "__main__":
    main()
