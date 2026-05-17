import pytest
import requests

PET_BASE_URL = "http://5.181.109.28:9090/api/v3"
STORE_BASE_URL = "http://5.181.109.28:9090/api/v3/store"


@pytest.fixture(scope="function")
def create_pet():
    payload = {"id": 1,
               "name": "Buddy",
               "status": "available"}

    response = requests.post(f"{PET_BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="function")
def create_order():
    payload = {"id": 1,
               "petId": 1,
               "quantity": 1,
               "status": "placed",
               "complete": True}

    response = requests.post(f"{STORE_BASE_URL}/order", json=payload)
    assert response.status_code == 200
    return response.json()
