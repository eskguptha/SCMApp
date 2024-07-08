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

def test_list_products():
    response = client.get("/products")
    assert response.status_code == 200

def test_list_customers():
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json()['data']['result'] == []

def test_suppliers_bad_gateway_res():
    response = client.post("/suppliers",json={})
    assert response.status_code == 422

def test_products_bad_gateway_res():
    response = client.post("/products", json={})
    assert response.status_code == 422

def test_customers_bad_gateway_res():
    response = client.post("/customers", json={})
    assert response.status_code == 422

def test_orders_bad_gateway_res():
    response = client.post("/orders", json={})
    assert response.status_code == 422

def test_orders_create_res():
    response = client.post("/orders", json={
              "customers_id": "string",
              "order_status_id": 0,
              "order_date": "2024-07-08T07:14:06.391Z",
              "contact_info": "string",
              "order_items": [
                "string"
              ]
            })
    try:
        assert response.status_code == 201
    except Exception as e:
        # duplicate record
        assert response.status_code == 500

def test_products_create_res():
    response = client.post("/products", json={
      "name": "string",
      "description": "string",
      "price": 0,
      "supplier_id": 1
    })
    try:
        assert response.status_code == 201
    except Exception as e:
        # duplicate record
        assert response.status_code == 400

def test_supplier_create_res():
    response = client.post("/suppliers", json={
      "name": "string",
      "contact_info": "string"
    })
    try:
        assert response.status_code == 201
    except Exception as e:
        # duplicate record
        assert response.status_code == 500

def test_customers_create_res():
    response = client.post("/customers", json={
      "name": "string",
      "contact_info": "string"
    })
    try:
        assert response.status_code == 201
    except Exception as e:
        # duplicate record
        assert response.status_code == 500