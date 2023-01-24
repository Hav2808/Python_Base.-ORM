import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Sale, Stock, Book, Shop




DSN = 'postgresql://postgres:Hawk43601$@localhost:5432/CLIENT_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures', 'r') as fd:
  data = json.load(fd)

for record in data:
  model = {
    'publisher': Publisher,
    'shop': Shop,
    'book': Book,
    'stock': Stock,
    'sale': Sale,
  }[record.get('model')]
  session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

for c in session.query(Sale).all():
  print(c)

print("*"*100)

for c in session.query(Book).all():
  print(c)

print("*"*100)

for c in session.query(Publisher).all():
  print(c)

print("*"*100)

for c in session.query(Stock).all():
  print(c)

print("*"*100)

for c in session.query(Shop).all():
  print(c)


selected_publisher = input("Укажите имя издателя: ")

for с in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale). join(Publisher).join(Stock).join(Shop).join(Sale). filter(Publisher.name == selected_publisher):
    print(f'{с.title} | {с.name} | {str(с.price)} | {с.date_sale}')


session.close()
