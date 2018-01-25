from utils import get_top100_list, get_song_detail


if __name__ == '__main__':
    top100_result = get_top100_list()
    for item in top100_result:
        print(item)

    print('-' * 200)
    detail_result = get_song_detail(30755375)
    print(f'song_name = {detail_result["song_name"]}')
    print(f'artist = {detail_result["artist"]}')
    print(f'album = {detail_result["album"]}')
    print(f'release_date = {detail_result["release_date"]}')
    print(f'genre = {detail_result["genre"]}')
    print(f'flac = {detail_result["flac"]}')
    print(f'lyric = {detail_result["lyric"]}')
    print(f'lyricist = {detail_result["lyricist"]}')
    print(f'composer = {detail_result["composer"]}')
    print(f'arranger = {detail_result["arranger"]}')
