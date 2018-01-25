import re

from bs4 import BeautifulSoup
from utils import get_top100_list


# source = open('melon.html', 'rt').read()
# soup = BeautifulSoup(source, 'lxml')
#
# result = []
#
# for tr in soup.find_all('tr', class_='lst50'):
#
#     rank = tr.find('span', class_='rank').text
#     img_url = tr.find('a', class_='image_typeAll').find('img').get('src')
#     title = tr.find('div', class_='rank01').find('a').text
#     artist = tr.find('div', class_='rank02').find('a').text
#     album = tr.find('div', class_='rank03').find('a').text
#
#     # .* -> 임의 문자의 최대 반복
#     # \. -> '.' 문자
#     # .*? -> '/'이 나오기전까지의 최소 반복
#     p = re.compile(r'(.*\..*?)/')
#     img_url = re.search(p, img_url).group(1)
#
#     result.append({
#         'rank': rank,
#         'img_url': img_url,
#         'title': title,
#         'artist': artist,
#         'album': album,
#     })
#
# for i in result:
#     print(i)


if __name__ == '__main__':
    result = get_top100_list()
    # for item in result:
    #     print(item)