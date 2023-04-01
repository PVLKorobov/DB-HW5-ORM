import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import json


Base = declarative_base()

class publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

class book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(publisher, backref='book')

class shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

class stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(book, backref='stock')
    shop = relationship(shop, backref='stock')

class sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Double, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(stock, backref='sale')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def fill_tables(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    with open('tests_data.json', 'r') as dataFile:
        entriesToAdd = []
        data = json.load(dataFile)
        for entry in data:
            if entry['model'] == 'publisher':
                entriesToAdd.append(publisher(id=entry['pk'], name=entry['fields']['name']))
            elif entry['model'] == 'book':
                entriesToAdd.append(book(id=entry['pk'], title=entry['fields']['title'], id_publisher=entry['fields']['id_publisher']))
            elif entry['model'] == 'shop':
                entriesToAdd.append(shop(id=entry['pk'], name=entry['fields']['name']))
            elif entry['model'] == 'stock':
                entriesToAdd.append(stock(id=entry['pk'], id_book=entry['fields']['id_book'], id_shop=entry['fields']['id_shop'], count=entry['fields']['count']))
            else:
                entriesToAdd.append(sale(id=entry['pk'], price=entry['fields']['price'], date_sale=entry['fields']['date_sale'], count=entry['fields']['count'], id_stock=entry['fields']['id_stock']))
        session.add_all(entriesToAdd)
        session.commit()
    session.close()

def find_sales(engine, publisherId=None, publisherName=None):
    Session = sessionmaker(bind=engine)
    session = Session()

    if publisherId != None:
        print(f'Результат поиска по id: {publisherId}')
        for c in session.query(publisher, book, stock, sale, shop).join(book.publisher).join(stock).join(sale).join(shop).filter(publisher.id == publisherId).all():
            print('{:40s} | {:10s} | {:0.3f} | {}'.format(c[1].title, c[4].name, c[3].price, c[3].date_sale))
    elif publisherName != None:
        print(f'Результат поиска по name: {publisherName}')
        for c in session.query(publisher, book, stock, sale, shop).join(book.publisher).join(stock).join(sale).join(shop).filter(publisher.name == publisherName).all():
            print('{:40s} | {:10s} | {:0.3f} | {}'.format(c[1].title, c[4].name, c[3].price, c[3].date_sale))
    print()