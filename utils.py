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
    url_chart_realtime_50 = 'https://www.melon.com/chart/index.htm'
    url_chart_realtime_100 = 'https://www.melon.com/chart/index.htm#params%5Bidx%5D=51'

    file_path = os.path.join(path_data_dir, 'chart_realtim_50.html')
    try:
        with open(file_path, 'xt') as f:
            response = requests.get(url_chart_realtime_50)
            f.write(response.text)
    except FileExistsError:
        print(f'"{file_path}" file is already exists!')

    file_path = os.path.join(path_data_dir, 'chart_realtim_100.html')
    if not os.path.exists(file_path):
        response = requests.get(url_chart_realtime_100)
        with open(file_path, 'wt') as f:
            f.write(response.text)
    else:
        print(f'"{file_path}" file is already exists!')


get_top100_list()
