import sqlite3 as sqlite
import json

conn = sqlite.connect('books.db') # Creation of a new database
cursor = conn.cursor() # Cursor creation

query_file = open("./queries/books_table_creation.sql")
query = query_file.read()
query_file.close()

print("Creazione tabella Books...")
try:
    cursor.execute(query)
    conn.commit()
    print("Tabella creata!")
except Exception as exc:
    print(exc)

books_json = open('books.json')
books_list = json.load(books_json)
books_json.close()

query_books = [f"(\"{book['title']}\", \"{book['author']}\", {book['year_published']})" for book in books_list]
insert_query = 'INSERT INTO Books (title, author, year_published) VALUES '+" ,".join(query_books)+";"

print("Inserimento dati...")

cursor.execute(insert_query)
conn.commit()

print("Dati inserit!")

cursor.close()
conn.close()
