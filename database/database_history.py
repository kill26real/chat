import sqlite3 as sq


def init_db():
    with sq.connect('history.db') as base:
        cur = base.cursor()

        # cur.execute("DROP TABLE IF EXISTS history")

        cur.execute("""CREATE TABLE IF NOT EXISTS history(
        user_name TEXT,
        command TEXT,
        date DATE,
        city TEXT,
        hotels_names TEXT
        )""")
