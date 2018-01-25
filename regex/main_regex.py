import requests
import re

# response = requests.get('https://www.melon.com/chart/index.htm')
# print(response.status_code)
# print(response.encoding)
# print(response.text)

melon = '''
<div class="wrap">
    <div class="wrap_song_info">
        <div class="ellipsis rank01"><span>
            <a href="javascript:melon.play.playSong('19030101',30851703);" title="다른사람을 사랑하고 있어 재생">다른사람을 사랑하고 있어</a>
            </span>
        </div>
        <br>
        <div class="ellipsis rank02">
            <a href="javascript:melon.link.goArtistDetail('514741');" title="수지 (SUZY) - 페이지 이동">수지 (SUZY)</a><span class="checkEllipsis" style="display: none;"><a href="javascript:melon.link.goArtistDetail('514741');" title="수지 (SUZY) - 페이지 이동">수지 (SUZY)</a></span>
        </div> 
    </div>
</div>
'''
# p1 = re.compile(r'<div class="ellipsis rank01">([\w\W]*?)</div>')
p1 = re.compile(r'<div class="ellipsis rank01">(.*?)</div>', re.DOTALL)
rank01 = re.search(p1, melon).group()
print(rank01)

p2 = re.compile(r'<a.*?>(.*?)</a>', re.DOTALL)
rank02 = re.search(p2, rank01).group(1)
print(rank02)
