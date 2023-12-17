import os

from dotenv import load_dotenv
import psycopg2

load_dotenv()

# Подключаемся к БД
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(url)

CREATE_METRO = ("CREATE TABLE IF NOT EXISTS metros ("
                "id SERIAL PRIMARY KEY NOT NULL,"
                "name TEXT);")

CREATE_REOBJECT = ("CREATE TABLE IF NOT EXISTS re_object "
                   "(id SERIAL PRIMARY KEY NOT NULL,"
                   "name TEXT,"
                   "address TEXT NULL,"
                   "floor INTEGER NULL,"
                   "area INTEGER NULL,"
                   "obj_type TEXT);")

CREATE_TABLE_METRO_REOBJECT = ("CREATE TABLE IF NOT EXISTS metro_re_object "
                               "(metro_id INTEGER REFERENCES metros (id) ON UPDATE CASCADE ON DELETE CASCADE,"
                               "reobject_id INTEGER REFERENCES re_object (id) ON UPDATE CASCADE ON DELETE CASCADE,"
                               "CONSTRAINT metro_re_object_pkey PRIMARY KEY (metro_id, reobject_id) );")

INSERT_METRO = "INSERT INTO metros (name) VALUES (%s) RETURNING name;"
INSERT_REOBJECT = ("INSERT INTO re_object (name, address, floor, area, obj_type) VALUES (%s, %s, %s, %s, %s) "
                   "RETURNING id;")
INSERT_METRO_REOBJECT = "INSERT INTO metro_re_object (metro_id, reobject_id) VALUES (%s, %s);"


def db_all_metros():
    """Вывод всех метро в базе"""
    with connection:
        with connection.cursor() as cur:
            cur.execute(CREATE_METRO)
            cur.execute(CREATE_REOBJECT)
            cur.execute(CREATE_TABLE_METRO_REOBJECT)
            cur.execute("SELECT * FROM metros")
            all_metros = [m[1] for m in cur.fetchall() if m]
    return all_metros


def db_all_re_objects():
    """Вывод всех объектов недвижимости в базе"""
    with connection:
        with connection.cursor() as cur:
            cur.execute(CREATE_METRO)
            cur.execute(CREATE_REOBJECT)
            cur.execute(CREATE_TABLE_METRO_REOBJECT)
            cur.execute("SELECT * FROM re_object")
            all_re_objects = cur.fetchall()
    return all_re_objects


def db_filter_re_objects(s_area, s_floor, s_metro):
    """Фильтрация объектов недвижимости в базе"""
    all_re_objects = []
    if s_metro:
        with connection:
            with connection.cursor() as cur:
                cur.execute(CREATE_METRO)
                cur.execute(CREATE_REOBJECT)
                cur.execute(CREATE_TABLE_METRO_REOBJECT)
                cur.execute(f"SELECT re_object.id, re_object.name, re_object.address, re_object.floor, re_object.area "
                            f"FROM metro_re_object "
                            f"INNER JOIN re_object ON metro_re_object.reobject_id = re_object.id "
                            f"INNER JOIN metros ON metros.id = metro_re_object.metro_id "
                            f"WHERE metros.name LIKE '%{s_metro}%'"
                            f"AND floor >= {s_floor}"
                            f"AND area >= {s_area} ;")
                all_re_objects = cur.fetchall()
    else:
        with connection:
            with connection.cursor() as cur:
                cur.execute(CREATE_METRO)
                cur.execute(CREATE_REOBJECT)
                cur.execute(CREATE_TABLE_METRO_REOBJECT)
                cur.execute(f"SELECT * FROM re_object WHERE area >= {s_area} "
                            f"AND floor >= {s_floor};")
                all_re_objects = cur.fetchall()
    return all_re_objects


def db_re_objects_by_id(id):
    """Вывод объекта недвижимости по id"""
    with connection:
        with connection.cursor() as cur:
            cur.execute(CREATE_METRO)
            cur.execute(CREATE_REOBJECT)
            cur.execute(CREATE_TABLE_METRO_REOBJECT)
            cur.execute(f"SELECT * FROM re_object WHERE id={id}")
            re_object = cur.fetchone()
    return re_object


def db_add_metro(name):
    """Добавить новое метро базу"""
    with connection:
        with connection.cursor() as cur:
            cur.execute(CREATE_METRO)
            cur.execute(INSERT_METRO, (name,))
    return True


def db_re_object_metros(id):
    """Вывод всех метро по id объекта недвижимости"""
    with connection:
        with connection.cursor() as cur:
            cur.execute(f"SELECT metro_id FROM metro_re_object WHERE reobject_id = {id} ;")
            metro_ids = tuple(id[0] for id in cur.fetchall() if id)
            if not metro_ids:
                return []
            cur.execute(f"SELECT name FROM metros WHERE id IN {metro_ids} ;")
            metro_names = [id[0] for id in cur.fetchall() if id]
            return metro_names


def db_add_re_object(name, address, floor, area, obj_type, metro):
    """Добавит объект недвижмости"""
    with connection:
        with connection.cursor() as cur:
            cur.execute(CREATE_REOBJECT)

            # создаём объект
            cur.execute(INSERT_REOBJECT, (name, address, floor, area, obj_type))
            new_re_object_id = cur.fetchone()[0]

            # создаём связь объекта с метро
            if metro:
                metro = tuple(metro)
                cur.execute(f'SELECT id from metros WHERE name IN {metro}')
                all_metro_ids = cur.fetchall()
                for m_id in all_metro_ids:
                    cur.execute(INSERT_METRO_REOBJECT, (m_id[0], new_re_object_id))
        return True
