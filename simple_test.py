import pytest
from fastapi.testclient import TestClient
from src.controllers import user_management, message_management
from src.models.schema.user import UserResponse, UserRequest, UserRequestUpdatable
from src.models.schema.message import UserMessageRequest
from main import app
# client = TestClient(user_management.router)
from fastapi.encoders import jsonable_encoder
client = TestClient(app=app)

"""
def add(a,b):
    return a + b

def test_user_fullname(userSample):
    assert userSample.fullname == "test1"

@pytest.mark.parametrize("a,b,result", [(2, 3, 5), (0, 0, 0)])
def test_add(a, b, result):
    assert add(a, b) == result

def test_insert_user():
    currentUser =  UserRequest(
        fullname="test1", 
        username="test_username1", 
        email="test1@test.se", 
        phone_number="0765864341")
    response = client.post("/user",json=jsonable_encoder(currentUser))
    print("response")
    print(response)
    # assert response.status_code == 200
    assert response.json() == {
        "username": "test_username1", 
        "email": "test1@test.se", 
        "phone_number": "0765864341"
    }
"""
@pytest.fixture
def userSample():
    return UserRequest(
        fullname="test1", 
        username="test_username1", 
        email="test1@test.se", 
        phone_number="0765864341")

@pytest.fixture
def messageSample(userSample):
    return UserMessageRequest(
        email_recipient=userSample.email,
        subject= "Tech",
        content= "Let's talk about tech")

def test_insert_user(userSample):
    """
        response = client.post("/endpoint",json={
            "dt": 10.0,
        })
    """
    response = client.post("/user",json=jsonable_encoder(userSample))
    print("response")
    print(response)
    assert response.status_code == 201
    assert response.json() == {
        "username": "test_username1", 
        "email": "test1@test.se", 
        "phone_number": "0765864341"
    }


def test_send_msg(messageSample):
    response = client.post("/message",json=jsonable_encoder(messageSample))
    assert response.status_code == 202

def test_fetch_all_msg():
    response = client.get("/message?sortDir=asc&page_number=1&page_size=3")
    assert response.status_code == 200

def test_fetch_new_msg():
    response = client.get("/message/new")
    assert response.status_code == 200

def test_fetch_new_msg():
    response = client.delete("/message/1")
    assert response.status_code == 204
    
def test_fetch_new_msg():
    response = client.delete("/message/1")
    assert response.status_code == 204

def test_send_multiple_msg(messageSample):
    for i in range(4):
        response = client.post("/message",json=jsonable_encoder(messageSample))
        assert response.status_code == 202

def test_delete_multiple_msg(messageSample):
    response = client.delete("/message?ids=1,2,3,4")
    assert response.status_code == 204

def test_fetch_all_msg_and_size_zero():
    response = client.get("/message?sortDir=asc&page_number=1&page_size=100")
    assert response.json()["data"] == []
