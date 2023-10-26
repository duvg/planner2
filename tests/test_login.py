import httpx
import pytest
from typing import AsyncGenerator
from models.user import User

@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient)  -> None:
  payload = {
    "email": "testuser@mail.com",
    "password": "testpassword"
  }

  headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
  }

  test_response = {
    "message": "User successfully registered!"
  }

  response = await default_client.post("/users/signup", json=payload, headers=headers)

  assert response.status_code == 200
  assert response.json() == test_response

@pytest.mark.asyncio
async def test_sing_user_in(default_client: httpx.AsyncClient) -> None:
  payload = {
    "username": "testuser@mail.com",
    "password": "testpassword"
  }

  headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
  }

  response = await default_client.post("/users/signin", data=payload, headers=headers)

  assert response.status_code == 200
  assert response.json()["token_type"] == "Bearer"
