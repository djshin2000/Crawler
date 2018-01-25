import os
import re
import requests
from bs4 import BeautifulSoup


def get_top100_list(refresh_html=False):
    """
    실시간 차트 1~100위의 리스트 반환
    파일위치:
        data/chart_realtime.html
    :param refresh_html: True일 경우, 무조건 새 HTML파일을 사이트에서 받아와 덮어씀
    :return:
    """
    # util.py의 위
    path_module = os.path.abspath(__name__)

    # 프로젝트 컨테이너 폴더 경로치
    root_dir = os.path.dirname(path_module)

    # data/ 폴더 경로
    path_data_dir = os.path.join(root_dir, 'data')

    # data 폴더가 없을 경우 생성
    os.makedirs(path_data_dir, exist_ok=True)

    # 웹페이지 주소
    url_chart_realtime = 'https://www.melon.com/chart/index.htm'

    # refresh_html 매개변수가 True일 경우, 무조건 새로 파일을 다운받도록 함
    file_path = os.path.join(path_data_dir, 'chart_realtime.html')
    try:
        with open(file_path, 'wt' if refresh_html else 'xt') as f:
            response = requests.get(url_chart_realtime)
            f.write(response.text)
    except FileExistsError:
        print(f'"{file_path}" file is already exists!')

    # *.html File Open
    source = open(file_path, 'rt').read()
    soup = BeautifulSoup(source, 'lxml')

    result = []

    for tr in soup.find_all('tr', class_=['lst50', 'lst100']):
        rank = tr.find('span', class_='rank').text
        img_url = tr.find('a', class_='image_typeAll').find('img').get('src')
        title = tr.find('div', class_='rank01').find('a').text
        artist = tr.find('div', class_='rank02').find('a').text
        album = tr.find('div', class_='rank03').find('a').text

        # .* -> 임의 문자의 최대 반복
        # \. -> '.' 문자
        # .*? -> '/'이 나오기전까지의 최소 반복
        p = re.compile(r'(.*\..*?)/')
        img_url = re.search(p, img_url).group(1)

        result.append({
            'rank': rank,
            'img_url': img_url,
            'title': title,
            'artist': artist,
            'album': album,
            # 'song_id': song_id,
        })

    return result
