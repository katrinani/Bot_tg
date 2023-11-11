import sqlite3 as sq


async def db_start():
    conn = sq.connect('database.db')
    cur = conn.cursor()  # объект "cursor" для выполнения SQL-запросов и операций с базой данных
    cur.execute('''
    CREATE TABLE IF NOT EXISTS profile (
    user_id TEXT PRIMARY KEY, 
    user_group TEXT,
    user_mess TEXT
    )
    ''')
    conn.commit()  # cохраняем изменения


async def create_profile(user_id):
    conn = sq.connect('database.db')
    cur = conn.cursor()
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?,?,?)", (user_id, '', ''))
        conn.commit()


async def edit_profile(user_group, user_id):
    conn = sq.connect('database.db')
    cur = conn.cursor()
    cur.execute("UPDATE profile SET user_group == '{}' WHERE user_id == '{}'".format(
        user_group, user_id))
    conn.commit()


async def check_group_of_student(user_id: int) -> str:
    conn = sq.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"SELECT user_group FROM profile WHERE user_id == '{user_id}'")
    user_group = cur.fetchone()
    conn.commit()
    return user_group[0]


async def add_remind(mess, user_id):
    conn = sq.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"UPDATE profile SET user_mess == '{mess}' WHERE user_id == '{user_id}'")
    conn.commit()


async def remind_mess(user_id: int) -> str:
    conn = sq.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"SELECT user_mess FROM profile WHERE user_id == '{user_id}'")
    user_mess = cur.fetchone()
    conn.commit()
    return user_mess[0]
