import re
import requests

__all__ = (
    'get_tag_attribute',
    'get_tag_content',
    'find_tag',
)

tag_str = '''
<div class="top_right ">
    <ul class="clfix">

        <li class="first_child"><a href="/commerce/pamphlet/web/sale_listMainView.htm" title="이용권구매" class="menu01 mlog" data="LOG_PRT_CODE=1&MENU_PRT_CODE=0&MENU_ID_LV1=&CLICK_AREA_PRT_CODE=B01&ACTION_AF_CLICK=V1"><span>이용권구매</span></a></li>

        <li><a href="/event/vip/index.htm" title="VIP혜택관" class="menu02 mlog" data="LOG_PRT_CODE=1&MENU_PRT_CODE=0&MENU_ID_LV1=&CLICK_AREA_PRT_CODE=V06&ACTION_AF_CLICK=V1"><span>VIP혜택관</span></a></li>

        <li class="last_child"><a href="/event/index.htm" title="이벤트" class="menu03 mlog" data="LOG_PRT_CODE=1&MENU_PRT_CODE=0&MENU_ID_LV1=&CLICK_AREA_PRT_CODE=B03&ACTION_AF_CLICK=V1"><span>이벤트</span></a></li>
    </ul>
</div>'''


def save_file():
    response = requests.get('https://www.melon.com/chart/index.htm')
    with open('melon.html', 'wt') as f:
        f.write(response.text)
    f.close()


def get_tag_attribute(attribute_name, tag_string):
    pattern = re.compile(r'^.*?<.*?{}.*?=.*?"(?P<value>.*?)".*?>'.format(attribute_name), re.DOTALL)
    result = re.search(pattern, tag_string).group('value')
    if result:
        return result
    return ''
# print(get_tag_attribute('class', tag_str))


def get_tag_content(tag_string):
    p = re.compile(r'<.*?>(?P<value>.*)</.*?>', re.DOTALL)
    m = re.search(p, tag_str)
    if m:
        return get_tag_content(m.group('value'))
    elif re.search(r'[<>]', tag_string):
        return ''
    return tag_string
# print(get_tag_content(tag_str))


def find_tag(tag, tag_string, class_=None):
    p = re.compile(r'.*?(<{tag}.*?{class_}.*?>.*?</{tag}>)'.format(
        tag=tag,
        class_=f'class=".*?{class_}.*?"' if class_ else '',
    ), re.DOTALL)
    m = re.search(p, tag_string)
    if m:
        return m.group(1)
    return None
