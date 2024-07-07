from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_pong():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}

def test_list_suppliers():
    response = client.get("/suppliers")
    assert response.status_code == 200
    assert response.json()['data']['result'] == []

def test_list_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json()['data']['result'] == []

def test_suppliers_bad_token():
    response = client.post("/suppliers",json={})
    assert response.status_code == 400
    assert response.json()['status'] == "NotOK"

def test_products_bad_token():
    response = client.post("/products", json={})
    assert response.status_code == 400
    assert response.json()['status'] == "NotOK"

def test_orders_bad_token():
    response = client.post("/orders", json={})
    assert response.status_code == 400
    assert response.json()['status'] == "NotOK"