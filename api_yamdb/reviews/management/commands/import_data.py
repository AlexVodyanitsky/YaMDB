import csv
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()

        with open('static/data/genre.csv', 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['id'], i['name'], i['slug']) for i in dr]
        insert_records = ("INSERT INTO reviews_genre "
                          "(id, name, slug) VALUES (?, ?, ?);")
        cursor.executemany(insert_records, to_db)

        with open('static/data/category.csv', 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['id'], i['name'], i['slug']) for i in dr]
        insert_records = ("INSERT INTO reviews_category "
                          "(id, name, slug) VALUES (?, ?, ?);")
        cursor.executemany(insert_records, to_db)

        with open('static/data/titles.csv', 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['id'], i['name'], i['year'], i['category'])
                     for i in dr]
        insert_records = ("INSERT INTO reviews_title "
                          "(id, name, year, category_id) VALUES (?, ?, ?, ?);")
        cursor.executemany(insert_records, to_db)

        connection.commit()
        connection.close()
