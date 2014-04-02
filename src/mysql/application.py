from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine("mysql+mysqldb://raijin@127.0.0.1/newsnet_db?charset=utf8&use_unicode=1")
