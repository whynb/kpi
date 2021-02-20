# coding: utf-8

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import *
from jx.util import *
from pymysql.err import *
from typing import List


# engine = create_engine('sqlite:///data.db', echo=True)
engine = create_engine('mysql+pymysql://root:password@localhost:3306/kpi?charset=utf8', echo=True)
Database = sessionmaker(bind=engine)
db = Database()

conn = engine.raw_connection()
cursor = conn.cursor()

Base = declarative_base()
