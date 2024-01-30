import sqlite3
import datetime 
              
conn = sqlite3.connect('watch_list_data.sqlite')
cur = conn.cursor()

def create_tables():
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        user_name TEXT,
        user_email TEXT,
        user_password TEXT
    ); 
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT,
        release_timestamp REAL
    );
    CREATE TABLE IF NOT EXISTS watched (
        user_id INTEGER,
        movie_id INTEGER,
        PRIMARY KEY(user_id,movie_id)
    )
    ''')
    conn.commit()
    
def add_user(user_name,user_email,user_password):
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    for row in rows:
        if row[1] == user_name:
            return 'User name is taken!'
            break
        if row[2] == user_email:
            return 'Email is taken'
            break
    cur.execute('''INSERT INTO users 
        (user_name,user_email,user_password) VALUES ( ?, ?, ? )''', (user_name, user_email, user_password ))
    conn.commit()
    cur.execute('SELECT * FROM users')
    checks = cur.fetchall()
    for check in checks:
        if check[1] == user_name and check[2] == user_email:
            print()
            print('Created successfully')
            print()
            break 
        
def fetch_hash_password(user_email):
    cur.execute('SELECT user_password FROM users WHERE user_email = ?', (user_email, ))
    try:
       stored_hash = cur.fetchone()[0]
       return stored_hash
    except TypeError:
        pass 
            
def add_movie(title, release_timestamp):
    cur.execute( '''INSERT INTO movies 
        (title,release_timestamp) VALUES ( ?, ? )''',(title, release_timestamp))
    conn.commit()
    
def get_user_id(user_name):
    cur.execute('SELECT id FROM users WHERE user_name = ?', (user_name, ))
    try:
        user_id = cur.fetchone()[0]
        return user_id
    except: #TypeError:
        pass
        
def get_movie_id(movie_title):
    cur.execute('SELECT id FROM movies WHERE title = ? ', (movie_title, ))
    try:
        movie_id = cur.fetchone()[0]
        return movie_id
    except: #TypeError:
        pass
     
def get_movies(upcoming=False):
    if upcoming:
        today_timestamp = datetime.datetime.today().timestamp()
        cur.execute('''SELECT * FROM movies
            WHERE release_timestamp > ?''', (today_timestamp, ))
    else:
        cur.execute('SELECT * FROM movies')
    return cur.fetchall()

def add_to_watched(user_id, movie_id):
    cur.execute('''INSERT INTO watched
        (user_id,movie_id) VALUES ( ?, ?)''', (user_id, movie_id ))
    conn.commit()
     
def get_watched_movies(user_name):
    cur.execute('''SELECT users.user_name, movies.title  FROM users JOIN
        movies JOIN watched ON watched.user_id = users.id AND
        watched.movie_id = movies.id WHERE users.user_name = ? ''', (user_name, ))
    return cur.fetchall()

def get_searched_movie(search):
    cur.execute('SELECT * FROM movies WHERE title LIKE ?', (f'%{search}%', ))
    return cur.fetchall()
        
def update_username(new_username,email):
    cur.execute("UPDATE users SET user_name = ? WHERE user_email = ? ", (new_username, email))
    conn.commit()
    
def update_movies(new_movie,movie_id):
    cur.execute("UPDATE movies SET title = ? WHERE id = ?", (new_movie, movie_id))
    conn.commit()
    
def delete_account(email):
    cur.execute("DELETE FROM users WHERE user_email = ?", (email, ))
    conn.commit()

def delete_movie(movie_id):
    cur.execute("DELETE FROM movies WHERE id = ?", (movie_id, ))
    conn.commit()
    
def delete_watched_movie(user_id,movie_id):
    cur.execute("DELETE FROM watched WHERE user_id = ? and movie_id = ?", (user_id, movie_id))
    conn.commit()
    
def check_watched(user_id,movie_id):
    cur.execute("SELECT * FROM watched")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == user_id and row[1] == movie_id:
            return True
        