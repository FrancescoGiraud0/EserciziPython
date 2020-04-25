import requests

# URL api
URL = 'http://127.0.0.1:5000/api/v1/resources/books/all'

# invio richiesta
r = requests.get(url = URL)

# estrazione dati (primo elemento)
data = r.json()

print('-'*20)
print("Prova richiesta di tutta la libreria")
for d in data:
    print(d)

# URL api
URL = 'http://127.0.0.1:5000/api/v1/resources/books'

# parametri query
PARAMS = {'id' : 1}

# invio richiesta
r = requests.get(url = URL, params = PARAMS)

# estrazione dati (primo elemento)
data = r.json()

print('-'*20)
print("Prova ricerca per id")
for d in data:
    print(d)

# URL api
URL = 'http://127.0.0.1:5000/api/v1/resources/books/author'

# parametri query
PARAMS = {'author' : 'Ted'}

# invio richiesta
r = requests.get(url = URL, params = PARAMS)

# estrazione dati (primo elemento)
data = r.json()

print('-'*20)
print("Prova ricerca per autore")
for d in data:
    print(d)

# URL api
URL = 'http://127.0.0.1:5000/api/v1/resources/books/author'

# parametri query
PARAMS = {'author' : 'Albert-László Barabási', 'title':'Linked', 'year_published':2002}

# url creato: http://localhost:5000/api/v1/resources/books/new?author=Paul+Davies&title=Uno+strano+silenzio&year_published=2010

# invio richiesta
r = requests.get(url = URL, params = PARAMS)

print(f'\n{r.text}\n')

# reinvio richiesta la fine di testare il controllo di presenza nel db prima dell'inserimento
r = requests.get(url = URL, params = PARAMS)

print(f'\n{r.text}\n')
