'''Ищем в спотифае песни и добавляем в заданный плейлист.
Если песня не находится, добавляем ее в текстовый файл incorrect_songs.txt.'''
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from variables import spotipy_client_id, spotipy_client_secret, my_playlist_id
from vk_part import main as do_song_list


def write_bad_songs(bad_song_list):
    '''Записываем названия песен, которых не смогли найти в текстовый файл.'''
    with open('incorrect_songs.txt', 'w') as f:
        for i in bad_song_list:
            try:
                f.write('{}\n'.format(i))
            except:
                pass


def add_songs_to_pl(song_list):
    '''Добавляем песни из переданного списка в плейлист.
    URI плейлиста, spotipy_client_id, spotipy_client_secret можно указать в variables.py '''
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotipy_client_id,
                                                   client_secret=spotipy_client_secret,
                                                   redirect_uri='https://www.spotify.com/',
                                                   scope='playlist-modify-private playlist-modify-public'))
    time.sleep(4)
    id_track_list = []
    incorrect_songs = []
    for song in song_list:
        try:
            result_search = sp.search(q=song)
            id_track_list.append(result_search['tracks']['items'][0]['id'])
        except:
            incorrect_songs.append(song)
    number_of_added_audio = 0
    while len(id_track_list)> number_of_added_audio:
        sp.playlist_add_items(my_playlist_id, id_track_list[number_of_added_audio:number_of_added_audio+99])
        number_of_added_audio+=99
        time.sleep(2)
    return incorrect_songs


def main():
    song_list = do_song_list()
    write_bad_songs(add_songs_to_pl(song_list))


if __name__ == '__main__':
    main()
