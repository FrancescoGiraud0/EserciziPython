import requests

# URL api
URL = 'http://127.0.0.1:5000/api/v1/resources/books'

# parametri query
PARAMS = {'id' : 1}

# invio richiesta
r = requests.get(url = URL, params = PARAMS)

# estrazione dati (primo elemento)
data = r.json()[0]

print(data)
print(data['title'])
