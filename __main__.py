import csv
import pdb
import wget

from commons import *
from authorization import *
from spotify_functions import *

generate_code_authorize_spotify_api()
access_token = generate_access_token()

set_access_token(access_token)

top_ten_artists = get_top_ten_artists()
top_five_genres = get_top_five_genres(top_ten_artists)

playlist_data = get_data_playlist('37i9dQZF1DWWGFQLoP9qlv')
albun_img = playlist_data['img_portada']
wget.download(albun_img, "")
print(playlist_data)

create_csv_file(top_ten_artists, top_five_genres, playlist_data)
