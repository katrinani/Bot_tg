import sqlite3 as sq


async def db_start():
    global db, cur
    db = sqlite3.connect('my_database.db')
    cur = db.cursor()  # cоздаем таблицу users
    #  объект "cursor" для выполнения SQL-запросов и операций с базой данных
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Users (   
    user_id INTEGER PRIMARY KEY,
    group TEXT
    )
    ''')
    db.commit()  # cохраняем изменения


async def create_profile(user_id):
    user = cur.execute('SELECT 1 FROM profile WHERE user_id == "{key}"'.format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES('?,?,?)", (user_id, '', ''))
        db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profile SET group == '{}' WHERE user_id == '{}'".format(
            data['group'], user_id))
        db.commit()
