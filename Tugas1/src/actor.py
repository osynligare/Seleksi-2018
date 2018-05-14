from bs4 import BeautifulSoup as bs
import requests
import time


def get_actors():
    """
    get list of 25 best movie actors from tasteofcinema.com
    :return list of actors
    """
    actors = []

    # scrape all pages
    for i in range(1, 4):
        # request
        url = 'http://www.tasteofcinema.com/2017/the-25-best-actors-of-the-21st-century/' + str(i)
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers)

        # get html in soup
        soup = bs(response.text, 'html.parser')

        # getting actors' name
        for actor in soup.find(class_='content').find_all('p'):
            act = actor.find('span', {'style': 'font-family: Helvetica; font-size: 20px;'})
            if act is not None:
                if act.get_text() != 'Pages:  1 2 3' and act.get_text() != 'Pages: 1 2 3':
                    actors.append(act.get_text())

        time.sleep(0.5)

    # removing number from actors' name
    for i in range(len(actors)):
        if actors[i][3] == ' ':
            actors[i] = actors[i][4:]
        elif actors[i][2] == ' ':
            actors[i] = actors[i][3:]

    return actors

