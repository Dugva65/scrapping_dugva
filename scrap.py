import requests
    

url = ' https://developer.spotify.com/documentation/web-api/'


response = requests.get(url)
print (response)

if response:
    print('ok')

else:
    print('wrong!!')


print(response.headers)
print(response.text)







