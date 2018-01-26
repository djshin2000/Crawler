import os
import re
import requests
from bs4 import BeautifulSoup


def create_html(create_file_name, url, url_param=None, refresh_html=False):
    # util.py의 위
    path_module = os.path.abspath(__file__)

    # 프로젝트 컨테이너 폴더 경로치
    root_dir = os.path.dirname(path_module)

    # data/ 폴더 경로
    path_data_dir = os.path.join(root_dir, 'data')

    # data 폴더가 없을 경우 생성
    os.makedirs(path_data_dir, exist_ok=True)

    # 웹페이지 주소
    # web_page_url = url

    # refresh_html 매개변수가 True일 경우, 무조건 새로 파일을 다운받도록 함
    file_path = os.path.join(path_data_dir, create_file_name)
    try:
        with open(file_path, 'wt' if refresh_html else 'xt') as f:
            response = requests.get(url, url_param)
            f.write(response.text)
            # 만약 받은 파일의 길이가 지나치게 짧을 경우 예외를 일으키고 예외블럭에서 삭제
            file_length = f.write(response.text)
            if file_length < 10:
                raise ValueError('파일이 너무 짧습니다.')
    except FileExistsError:
        print(f'"{file_path}" file is already exists!')
    except ValueError:
        os.remove(file_path)
        print(f'"{file_path}" 파일을 삭제 하였습니다.')
        return

    return file_path


def get_top100_list():
    """
    실시간 차트 1~100위의 리스트 반환
    파일위치:
        data/chart_realtime.html
    :param refresh_html: True일 경우, 무조건 새 HTML파일을 사이트에서 받아와 덮어씀
    :return:
    """
    file_path = create_html(
        create_file_name='chart_realtime.html',
        url='https://www.melon.com/chart/index.htm',
    )

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
        song_id = tr.find('a', {'class': 'song_info'}).get('href')
        pattern_song_id = re.compile(r"goSongDetail\(\'(.*?)\'\)", re.DOTALL)
        song_id = re.search(pattern_song_id, song_id).group(1)

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
            'song_id': song_id,
        })

    return result


def get_song_detail(song_id):
    """
    song_id에 해당하는 곡 정보 dict를 반환
    위의 get_top100_list의 각 곡 정보에도 song_id가 들어가도록 추가
    http://www.melon.com/song/detail.htm?songId=30755375
    위 링크를 참조
    파일명
        song_detail_{song_id}.html
    :param song_id: 곡 정보 dict
    :return:
    """
    parmas = {'songId': song_id}
    url = 'https://www.melon.com/song/detail.htm'
    # response = requests.get(url, parmas)
    create_file_name = 'song_detail_' + str(song_id) + '.html'
    file_path = create_html(
        create_file_name=create_file_name,
        url=url,
        url_param=parmas,
    )

    # *.html File Open
    source = open(file_path, 'rt').read()
    soup = BeautifulSoup(source, 'lxml')

    song_name = soup.select_one('div.song_name > strong').next_sibling.strip() # strip()은 앞뒤공백제거
    # song_name = re.sub(r'^([\s\n]*)', '', song_name) # 앞공백제거
    # song_name = re.sub(r'([\s\n]*)$', '', song_name) # 뒤공백제거

    artist = soup.select_one('div.section_info a.artist_name > span:nth-of-type(1)').getText()

    test = soup.find()

    meta_list = soup.select('div.section_info div.meta dl.list dd')
    # dt, dd를 dictionary로 저장하여 데이터 정합성을 체크하여 저장이 되도록 수정
    album = meta_list[0].getText()
    release_date = meta_list[1].getText()
    genre = meta_list[2].getText()
    flac = meta_list[3].getText()

    lyric = str(soup.select_one('div.section_lyric div.lyric'))
    ppp = re.compile(r'^<div.*?>.*?<!.*?>(?P<value>.*?)\s</div>$', re.DOTALL)
    lyric = re.search(ppp, lyric).group('value')
    lyric = re.sub(r'^([\s\n]*)', '', lyric)  # 처음공백제거
    lyric = re.sub(r'<br/>', '\n', lyric) # br태그를 줄바꿈으로 변

    prdcr_list = soup.find('div', class_='section_prdcr').find('ul', class_='list_person').find_all('li')
    lyricist = []
    composer = []
    arranger = []
    for item in prdcr_list:
        item_type = item.select_one('div.meta span').getText()
        item_artist = item.select_one('div.artist > a').getText()
        if item_type == '작사':
            lyricist.append(item_artist)
        elif item_type == '작곡':
            composer.append(item_artist)
        elif item_type == '편곡':
            arranger.append(item_artist)
        else:
            print('type이 정의되지 않은 artist 입니다.')

    result = {
        'song_name': song_name,
        'artist': artist,
        'album': album,
        'release_date': release_date,
        'genre': genre,
        'flac': flac,
        'lyric': lyric,
        'lyricist': lyricist,
        'composer': composer,
        'arranger': arranger,
    }

    return result


def get_song_search_list(search_word):
    url_parmas = {
        'q': search_word,
        'section': 'song'
    }
    url = 'https://www.melon.com/search/song/index.htm'
    create_file_name = 'song_search_list_' + str(search_word) + '.html'
    file_path = create_html(
        create_file_name=create_file_name,
        url=url,
        url_param=url_parmas,
    )

    # *.html File Open
    source = open(file_path, 'rt').read()
    soup = BeautifulSoup(source, 'lxml')

    tr_song_list = soup.find('form', id='frm_defaultList').find('tbody').find_all('tr')
    search_list = []
    for tr in tr_song_list:
        title = tr.select_one('td.t_left > div.wrap > div.ellipsis a.fc_gray').get_text()
        # print(title)
        search_list.append(title)

    return search_list
