import os
import requests


def get_top100_list(refresh_html=False):

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


get_top100_list()
