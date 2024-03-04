import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres', password='123456789', host='localhost')
conn.autocommit = True

cursor = conn.cursor()
