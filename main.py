from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm


MAIN_WORDS_URLS = 'https://bezbukv.ru/mask/л****'


def get_soup(session, url) -> BeautifulSoup:
    response = session.get(url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, features='lxml')


def get_links(soup: BeautifulSoup):
    links = []

    pagination = soup.find('ul', attrs={'id': 'yw2'})
    pages_tags = pagination.find_all('li', attrs={'class': 'page'})

    for tag in pages_tags:
        a_teg = tag.find('a')
        href = a_teg['href']
        page_link = urljoin(MAIN_WORDS_URLS, href)
        links.append(page_link)

    return links


def get_words(soup: BeautifulSoup) -> list:
    words_tag = soup.find('div', attrs={'id': 'yw1'})
    div_tags = words_tag.find_all('div', attrs={'class': 'view'})

    words = []
    for tag in div_tags:
        word = tag.text.split()[1]
        if 'н' in word:
            words.append(word)

    return words


def process_results(words):
    missing_latters = []
    for letter in missing_latters:
        for index in reversed(range(len(words))):
            word = words[index]
            if letter in word:
                del words[index]

    #TODO: отсеивание слов в которых повторяется найденая буква - сделать
                # опциональной
    # for index in reversed(range(len(words))):
    #     word = words[index]
    #     if word.count('а') > 1:
    #         del words[index]

    return words


def main() -> None:
    #TODO: проведи рефакторинг. За основу возьми https://github.com/RolAlek/bs4_parser_pep/
    #TODO: продумай реализацию парсинга данных из терминала(команды):
        # указание маски;
        # добавление отсутсвующих в слове букв;
    #TODO: добавь очистку кэша если слово найдено
    #TODO: интеграция в ТГ-бот

    session = requests_cache.CachedSession()
    soup = get_soup(session, MAIN_WORDS_URLS)

    #TODO: вынеси проверку в утилиты
    if soup.find('div', attrs={'class': 'pagination'}):
        links: list[str] = get_links(soup)

        for link in links:
            words_soup = get_soup(session, link)
            row_list: list[str] = get_words(words_soup)
    else:
        row_list = get_words(soup)

    results = process_results(row_list)
    
    print(results)


if __name__ == '__main__':
    main()

