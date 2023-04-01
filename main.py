import sqlalchemy
import configparser
from models import create_tables, fill_tables, find_sales

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('database_config.ini')
    config = config['DEFAULT']
    engine = sqlalchemy.create_engine('postgresql://{name}:{password}@localhost:5432/{dbName}'.format(name=config['user_name'], password=config['user_password'], dbName=config['database_name']))

    create_tables(engine)
    fill_tables(engine)
    find_sales(engine, publisherId=1)
    find_sales(engine, publisherName='No starch press')