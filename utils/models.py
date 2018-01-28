import os
import re
import requests
from bs4 import BeautifulSoup
from utils import create_html


class MelonCrawler:
    # search_song을 이 클래스의 인스턴스 메서드로 추가
    def get_song_search_list(self, search_word):
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
            song_id = tr.select_one('td div.wrap.pd_none.left input[type=checkbox]').get('value')
            title = tr.select_one('td.t_left > div.wrap > div.ellipsis a.fc_gray').get_text()
            artist = tr.select_one('td.t_left div#artistName').get_text(strip=True)
            album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)
            search_list.append(
                Song(song_id=song_id, title=title, artist=artist, album=album)
            )

        return search_list


class Song:
    # __init__() 초기화 함수에 title, artist, album 정보를 받을 수 있도록 함
    def __init__(self, song_id, title, artist, album):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.album = album

        self._release_date = None
        self._lyrics = None
        self._genre = None
        self._lyricist = None
        self._composer = None
        self._arranger = None
        # self._producers = None

    def __str__(self):
        return f'{self.title} (아티스트: {self.artist}, 앨범: {self.album})'

    def get_detail(self):
        parmas = {'songId': self.song_id}
        url = 'https://www.melon.com/song/detail.htm'
        # response = requests.get(url, parmas)
        create_file_name = 'song_detail_' + str(self.song_id) + '.html'
        file_path = create_html(
            create_file_name=create_file_name,
            url=url,
            url_param=parmas,
        )

        # *.html File Open
        source = open(file_path, 'rt').read()
        soup = BeautifulSoup(source, 'lxml')

        song_name = soup.select_one('div.song_name > strong').next_sibling.strip()  # strip()은 앞뒤공백제거
        # song_name = re.sub(r'^([\s\n]*)', '', song_name) # 앞공백제거
        # song_name = re.sub(r'([\s\n]*)$', '', song_name) # 뒤공백제거

        artist = soup.select_one('div.section_info a.artist_name > span:nth-of-type(1)').getText()

        meta_list = soup.select('div.section_info div.meta dl.list dd')
        # dt, dd를 dictionary로 저장하여 데이터 정합성을 체크하여 저장이 되도록 수정
        album = meta_list[0].getText()
        release_date = meta_list[1].getText()
        genre = meta_list[2].getText()
        flac = meta_list[3].getText()

        lyrics = str(soup.select_one('div.section_lyric div.lyric'))
        ppp = re.compile(r'^<div.*?>.*?<!.*?>(?P<value>.*?)\s</div>$', re.DOTALL)
        lyrics = re.search(ppp, lyrics).group('value')
        lyrics = re.sub(r'^([\s\n]*)', '', lyrics)  # 처음공백제거
        lyrics = re.sub(r'<br/>', '\n', lyrics)  # br태그를 줄바꿈으로 변

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

        self.title = song_name
        self.artist = artist
        self.album = album
        self._release_date = release_date
        self._genre = genre
        self._lyrics = lyrics
        self._lyricist = lyricist
        self._composer = composer
        self._arranger = arranger

    @property
    def lyrics(self):
        if not self._lyrics:
            self.get_detail()
        return self._lyrics
