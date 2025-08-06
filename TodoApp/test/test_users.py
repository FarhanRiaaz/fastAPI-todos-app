from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user/get_user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "farhaanwirkX"
    assert response.json()['email'] == "farhaanwirk@gmail.comX"
    assert response.json()['first_name'] == "FarhanX"
    assert response.json()['last_name'] == "RiazX"
    assert response.json()['phone_number'] == "+923365510653X"
    assert response.json()['role'] == "Senior Software Engineer IIX"

def test_change_password_success(test_user):
    response = client.put("/user/update_passowrd",json={"password":"123456","new_password":"12345678"})
    
    assert response.status_code == status.HTTP_204_NO_CONTENT