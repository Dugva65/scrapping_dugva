import requests
    

url = 'https://accounts.spotify.com/api/token'


response = requests.get(url)
print (response)

if response:
    print('ok')

else:
    print('wrong!!')

#d = response.json()

#print(d['current_user_url'])
#print(response.headers)
