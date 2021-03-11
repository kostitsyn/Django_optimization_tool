import requests

r = requests.get('https://api.github.com/user', auth=('username', 'password'))

print(r.content)