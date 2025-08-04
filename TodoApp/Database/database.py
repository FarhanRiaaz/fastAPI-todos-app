from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#This setup is for sqlite database that is locally built and ready to use version 
SQLAlCHEMY_DATABASE_URL= 'sqlite:///./todosapp.db'
engine = create_engine(SQLAlCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})

#This setup is for MYSQL database and it's configurations are as follow:
#SQLAlCHEMY_DATABASE_URL= 'myaql+pymysql://root:password@127.0.0.1:61062/TodoApplicationDatabase'
#engine = create_engine(SQLAlCHEMY_DATABASE_URL)

#This setup is for POSTGRESS database and it's configurations are as follow:
#SQLAlCHEMY_DATABASE_URL= 'postgresql://postgres:@localhost/TodoApplicationDatabase'
#engine = create_engine(SQLAlCHEMY_DATABASE_URL)
 
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
 
Base = declarative_base()