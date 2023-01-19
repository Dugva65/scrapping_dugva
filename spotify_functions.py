import requests
import pdb
import csv

from commons import *

header_bear_token = {}

def set_access_token(token):
  global header_bear_token
  header_bear_token ={'Authorization': f"Bearer {token}"}

def get_top_ten_artists():
  response = requests.get(base_url + 'me/top/artists', params = {'limit' : 10},  headers=header_bear_token)
  return response.json()['items']

def get_top_five_genres(top_artists):
	top_five_genres = []
	for artist in top_artists:
		top_five_genres.append(artist['genres'])
		if len(top_five_genres) == 5:
			break 
	return top_five_genres

def get_data_playlist(playlist_id):
  response = requests.get(base_url + 'playlists/' + playlist_id,  headers=header_bear_token)
  response = response.json()
  playlist_information = {}
  playlist_information['img_portada'] = response["images"][0]['url']
  playlist_information['followers_number'] = response["followers"]['total']

  tracks_items = get_playlist_tracks(playlist_id)
  calculate_average_tracks(tracks_items, playlist_information)

  return playlist_information

def get_playlist_tracks(playlist_id):
  response = requests.get(base_url + 'playlists/' + playlist_id + '/tracks',  headers=header_bear_token)
  return response.json()['items']

def get_audio_analyses(track_id):
  response = requests.get(base_url + 'audio-analysis/' + track_id, headers=header_bear_token)
  return response.json()['track']

def get_audio_features(track_id):
  response = requests.get(base_url + 'audio-features/' + track_id, headers=header_bear_token)
  return response.json()

def calculate_average_tracks(tracks_items, play_list_information):
  count_items = 0
  tempo = 0
  acousticness = 0
  danceability = 0
  energy = 0
  instrumentalness = 0
  liveness = 0
  loudness = 0
  valence = 0

  for track_item in tracks_items:
    track_id = track_item['track']['id']
    print('.............')
    print(track_id)
    print('.............')
    audio_analyses_data = get_audio_analyses(track_id)
    audio_features_data = get_audio_features(track_id)
   
    count_items += 1
    tempo += audio_analyses_data["tempo"]
    acousticness += audio_features_data["acousticness"]
    danceability += audio_features_data["danceability"]
    energy += audio_features_data["energy"]
    instrumentalness += audio_features_data["instrumentalness"]
    liveness += audio_features_data["liveness"]
    loudness += audio_analyses_data["loudness"]
    valence += audio_features_data["valence"]
  
  play_list_information['average_tempo'] = tempo / count_items
  play_list_information['average_acousticness'] = acousticness / count_items
  play_list_information['average_danceability'] = danceability / count_items
  play_list_information['average_energy'] = energy / count_items
  play_list_information['average_instrumentalness'] = instrumentalness / count_items
  play_list_information['average_liveness'] = liveness / count_items
  play_list_information['average_loudness'] = loudness / count_items
  play_list_information['average_valence'] = valence / count_items

  return play_list_information

def create_csv_file(top_ten_artistis, top_five_genres, playlist_data):
  with open('data.csv', 'w') as f:
    writer = csv.writer(f)

    writer.writerow(top_ten_artistis)
    writer.writerow(top_five_genres)
    writer.writerow(playlist_data)

    f.close()