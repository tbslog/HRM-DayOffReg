import datetime
from datetime import date
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table, NVARCHAR, VARCHAR, DATETIME, FLOAT, cast, Date, String, BIGINT
# from sqlalchemy.orm import relationship
from sqlalchemy import types
# from setting import *
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import or_, and_
# from sqlalchemy import select
# from sqlalchemy import distinct
from sqlalchemy import create_engine, desc, distinct, and_
from sqlalchemy.engine.url import URL
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TINYINT

data_abc = dict(
    drivername='mssql',
    username='report2',
    password='Tbs123@',
    host='115.75.42.159',
    database='HRM',
    query={"driver": 'SQL Server Native Client 11.0'}
)

url = URL.create(**data_abc)

engine = create_engine(url=url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    return db

a= get_db

class Users(Base):
    __tablename__ = "Users"
    UserName = Column(VARCHAR(20),primary_key=True)
    EmpID = Column(BIGINT)
    Password= Column(VARCHAR(20))
    UserType= Column(TINYINT)
    Email = Column(VARCHAR(50))
    Status = Column(TINYINT)
    LastModify = Column(DATETIME)
    Modifier = Column(BIGINT)






