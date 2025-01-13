import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

def get_all_product():
    connection = sqlite3.connect('not_telegram.db')
    cursor = connection.cursor()
    get_all = cursor.execute('SELECT * FROM Products')
    products = get_all.fetchall()
    connection.commit()
    connection.close()
    return products


connection.commit()
connection.close()

