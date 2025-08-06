from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from ..database import Base
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..routers.todos import get_db,get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos,Users
from ..routers.auth import brcypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False},poolclass= StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind= engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'farhaanwirk','id':1,'role':'Senior Software Engineer II'}

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn to code!",
        description = "Need to learn everyday!",
        priority=5,
        id=1,
        complete=False,
        owner_id=1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="farhaanwirkX",
        email="farhaanwirk@gmail.comX",
        last_name="RiazX",
        first_name="FarhanX",
        phone_number="+923365510653X",
        role="Senior Software Engineer IIX",
        hashed_password=brcypt_context.hash("123456"),
        is_active=True,
    )
    db = TestingSessionLocal()
    
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
    
    
    