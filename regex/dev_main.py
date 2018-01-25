import re

# 파일읽기
# f = open('melon.txt', 'rt')
# melon = f.read()
# f.close()
source = open('melon.html', 'rt').read() # 이렇게 작성하면 close를 안써도 됨


# 정규 표현식을 이용하여 노래제목 찾기
p1 = re.compile(r'<div class="ellipsis rank01">(.*?)</div>', re.DOTALL)
p2 = re.compile(r'<a.*?>(.*?)</a>', re.DOTALL)
match = re.finditer(p1, source)
for i in match:
    print(re.search(p2, i.group()).group(1))



