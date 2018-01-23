# 'https://www.melon.com/chart/index.htm'의 내용을
# melon.txt 파일에 저장

import requests # alt + enter키


def save_file():
    response = requests.get('https://www.melon.com/chart/index.htm')
    with open('melon.html', 'wt') as f:
        f.write(response.text)
    f.close()


if __name__ == '__main__':
    save_file()
