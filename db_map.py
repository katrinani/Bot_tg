import sqlite3 as sq

# global conn, cur


async def db_start():
    # объявление, которое выполняется для всего текущего блока кода
    #  объект "cursor" для выполнения SQL-запросов и операций с базой данных
    conn = sq.connect('my_database.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS profile (
    user_id TEXT PRIMARY KEY, 
    user_group TEXT
    )
    ''')

    conn.commit()  # cохраняем изменения
    # conn.close()


async def create_profile(user_id):
    conn = sq.connect('my_database.db')
    cur = conn.cursor()
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?,?)", (user_id, ''))
        conn.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        conn = sq.connect('my_database.db')
        cur = conn.cursor()
        cur.execute("UPDATE profile SET user_group == '{}' WHERE user_id == '{}'".format(
            data['user_group'], user_id))
        conn.commit()
