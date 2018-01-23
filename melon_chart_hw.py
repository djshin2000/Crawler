import re

# 파일읽기
source = open('melon.html', 'rt').read() # 이렇게 작성하면 close를 안써도 됨

melon_chart = []

pattern_tbody = re.compile(r'<tbody>.*?</tbody>', re.DOTALL)
tbody_text = re.search(pattern_tbody, source).group()


pattern_tr = re.compile(r'<tr class="lst50".*?>.*?</tr>', re.DOTALL)
tr_text = re.findall(pattern_tr, tbody_text)
for idx_tr, tr in enumerate(tr_text):
    pattern_td = re.compile(r'<td.*?>.*?</td>', re.DOTALL)
    td_list = re.findall(pattern_td, tr)
    # for idx_td, td in enumerate(td_list):
    #     td_strip = re.sub(r'[\n\t]+|\s{2,}', '', td)

    chart_row = {}

    td_rank = td_list[1]
    pattern_rank = re.compile(r'<span class="rank.*?>(.*?)</span>', re.DOTALL)
    chart_rank = re.search(pattern_rank, td_rank).group(1)
    # print(chart_rank)
    chart_row['rank'] = chart_rank

    td_img_url = td_list[3]
    pattern_url = re.compile(r'img.*?src="(.*?)".*?>', re.DOTALL)
    img_url = re.search(pattern_url, td_img_url).group(1)
    # print(idx_tr, img_url)
    chart_row['img_url'] = img_url

    td_title_author = td_list[5]
    pattern_div_title = re.compile(r'<div class="ellipsis rank01">.*?</div>', re.DOTALL)
    pattern_title = re.compile(r'<a.*?>(.*?)</a>')
    div_title = re.search(pattern_div_title, td_title_author).group()
    title = re.search(pattern_title, div_title).group(1)
    # print(idx_tr, title)
    chart_row['title'] = title

    pattern_div_artist = re.compile(r'<div class="ellipsis rank02">.*?</div>', re.DOTALL)
    pattern_artist = re.compile(r'<a.*?>(.*?)</a>')
    div_artist = re.search(pattern_div_artist, td_title_author).group()
    artist = re.search(pattern_artist, div_artist).group(1)
    # print(idx_tr, artist)
    chart_row['artist'] = artist

    td_album = td_list[6]
    pattern_div_album = re.compile(r'<div class="ellipsis rank03">.*?</div>', re.DOTALL)
    pattern_album = re.compile(r'<a.*?>(.*?)</a>')
    div_album = re.search(pattern_div_album, td_album).group()
    album = re.search(pattern_album, div_album).group(1)
    # print(idx_tr, album)
    chart_row['album'] = album

    melon_chart.append(chart_row)



for i in melon_chart:
    print(i)
