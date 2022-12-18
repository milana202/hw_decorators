import os
import datetime
import requests
import re
from bs4 import BeautifulSoup
from fake_headers import Headers

def logger(old_function):
    def new_function(*args, **kwargs):
        with open('task3.log', 'a') as file:
            name = f'Function: {old_function.__name__}\n'
            file.write(name)
            start = str(datetime.datetime.now())
            file.write(f'{start}\n')
            argums = f'Arguments: {args}{kwargs}\n'
            file.write(argums)
            result = old_function(*args, **kwargs)
            file.write(f'Result: {result}\n')
        return result
    return new_function


url = "https://habr.com/ru/all/"
keywords = ['лет', 'фото', 'web', 'python']

def get_headers():
    return Headers(browser='firefox', os='win').generate()

def get_text(url):
    response = requests.get(url, headers=get_headers()).text
    return response

@logger
def parse_page(url, keywords):
    parced_list = []
    html = get_text(url)
    soup = BeautifulSoup(html, features='lxml')
    articles = soup.find_all(class_="tm-articles-list")
    for keyword in keywords:
        for article in articles:
            pattern = f".*?{keyword}.*?"
            result = re.search(pattern, article.text)
            if result != None:
                parced = {
                    "date": article.find("time")["title"],
                    "title": article.find("span").text,
                    "link": article.find("a")["href"]
                }
                parced_list.append(parced)
    print(parced_list)



if __name__ == '__main__':
    path = 'task3.log'
    if os.path.exists(path):
        os.remove(path)

    parced_page = parse_page(url, keywords)
