import psycopg2
from logs import log
from lxml import etree


# функция для подключения к базе данных
def db(os, version, architecture: str):
    # считываем информацию для подсоединения к базе данных из db.xml
    root = etree.parse('db.xml').getroot()

    try:
        # подсоединение к базе данных
        connection = psycopg2.connect(
            host=root[0].text,
            user=root[1].text,
            password=root[2].text,
            database=root[3].text
        )
        log('[INFO] Успешное подключение к базе данных')
        connection.autocommit = True

        # создаем таблицу(если ее нет)
        with connection.cursor() as cursor:
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS systems(
                    id SERIAL PRIMARY KEY,
                    os varchar(100),
                    version varchar(100),
                    architecture varchar(100))'''
            )

        # внесение данных в таблицу
        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO systems (os, version, architecture) VALUES('{os}' ,'{version}' , '{architecture}');"
            )
        log('[INFO] Успешное внесение данных в базу данных')

        connection.close()
    except Exception as e:
        # в случае ошибки логируем и возращаем ошибку
        log('[Error] Ошибка при работе с PostgreSQL ' + str(e))
        return 'error'
