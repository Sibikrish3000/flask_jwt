import pytest
from app import app, db, User
from flask_jwt_extended import decode_token
import logging
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def client():
    """Set up a test client and reset the database for each test."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory DB
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for testing
        yield client  # Run the test
        with app.app_context():
            db.drop_all()  # Clean up after test

def test_register(client):
    """Test user registration."""
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert b"User registered successfully!" in response.data

def test_register_existing_user(client):
    """Test registering a duplicate user."""
    client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 400
    assert b"Email already exists" in response.data

def test_login(client):
    """Test user login."""
    client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

def test_login_invalid_user(client):
    """Test login with invalid credentials."""
    response = client.post("/login", json={
        "email": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert b"Invalid credentials" in response.data

def test_protected_dashboard(client):
    """Test access to a protected route with a valid token."""
    client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    login_response = client.post("/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    access_token = login_response.get_json()["access_token"]

    response = client.get("/dashboard", headers={"Authorization": f"Bearer {access_token}"})
    print("Response Status Code:", response.status_code)
    print("Response Data:", response.get_json())

    assert response.status_code == 200
    assert b"Welcome testuser!" in response.data

def test_protected_dashboard_no_token(client):
    """Test access to a protected route without a token."""
    response = client.get("/dashboard")
    assert response.status_code == 401

