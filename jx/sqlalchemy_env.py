# coding: utf-8

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import *
from jx.util import *
from pymysql.err import *
from typing import List
from kpi import settings


# engine = create_engine('sqlite:///data.db', echo=True)
# engine = create_engine('mysql+pymysql://root:password@127.0.0.1:3306/kpi?charset=utf8', echo=True)
engine = create_engine('mysql+pymysql://%(user)s:%(pass)s@%(host)s:%(port)s/%(name)s?charset=utf8' % {
    'name': settings.DATABASES['default']['NAME'],
    'user': settings.DATABASES['default']['USER'],
    'pass': settings.DATABASES['default']['PASSWORD'],
    'host': settings.DATABASES['default']['HOST'],
    'port': settings.DATABASES['default']['PORT'],
}, echo=True)

Database = sessionmaker(bind=engine)
db = Database()

conn = engine.raw_connection()
cursor = conn.cursor()

Base = declarative_base()
