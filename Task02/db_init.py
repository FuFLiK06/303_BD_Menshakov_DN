import sqlite3
import csv
import os

# Имя базы данных
DB_NAME = 'movies_rating.db'

# Путь к папке с исходными данными (проверь, что папка dataset лежит на уровень выше Task02)
DATASET_DIR = '../dataset'

def create_tables(cursor):
    cursor.execute("DROP TABLE IF EXISTS movies")
    cursor.execute("DROP TABLE IF EXISTS ratings")
    cursor.execute("DROP TABLE IF EXISTS tags")
    cursor.execute("DROP TABLE IF EXISTS users")

    cursor.execute('''CREATE TABLE movies (
        id INTEGER PRIMARY KEY,
        title TEXT,
        genres TEXT
    )''')

    cursor.execute('''CREATE TABLE ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        rating REAL,
        timestamp INTEGER
    )''')

    cursor.execute('''CREATE TABLE tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        movie_id INTEGER,
        tag TEXT,
        timestamp INTEGER
    )''')

    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        gender TEXT,
        register_date TEXT,
        occupation TEXT
    )''')

def load_data(cursor):
    # Загрузка movies
    try:
        with open(os.path.join(DATASET_DIR, 'movies.csv'), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                cursor.execute("INSERT OR IGNORE INTO movies (id, title, genres) VALUES (?, ?, ?)", (row[0], row[1], row[2]))
    except FileNotFoundError:
        print("Внимание: файл movies.csv не найден!")

    # Загрузка ratings
    try:
        with open(os.path.join(DATASET_DIR, 'ratings.csv'), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                cursor.execute("INSERT INTO ratings (user_id, movie_id, rating, timestamp) VALUES (?, ?, ?, ?)", (row[0], row[1], row[2], row[3]))
    except FileNotFoundError:
         print("Внимание: файл ratings.csv не найден!")

    # Загрузка tags
    try:
        with open(os.path.join(DATASET_DIR, 'tags.csv'), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                cursor.execute("INSERT INTO tags (user_id, movie_id, tag, timestamp) VALUES (?, ?, ?, ?)", (row[0], row[1], row[2], row[3]))
    except FileNotFoundError:
         print("Внимание: файл tags.csv не найден!")

    # Загрузка users (предполагаем разделитель '|', как в стандартном MovieLens)
    try:
        with open(os.path.join(DATASET_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                row = line.strip().split('|')
                if len(row) >= 5:
                    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, gender, register_date, occupation) VALUES (?, ?, ?, ?, ?, ?)", (row[0], row[1], row[2], row[3], row[4], row[5]))
    except FileNotFoundError:
         print("Внимание: файл users.txt не найден!")

def main():
    print("Начинаю работу...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("Создание таблиц...")
    create_tables(cursor)

    print("Загрузка данных...")
    load_data(cursor)

    conn.commit()
    conn.close()
    print("База данных успешно создана и заполнена!")

if __name__ == '__main__':
    main()