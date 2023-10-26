import httpx
import pytest
from typing import AsyncGenerator, List

from auth.jwt_handler import create_access_token
from models.event import Event

@pytest.fixture(scope="module")
def access_token() -> str:
  return create_access_token("testuser@mail.com")

@pytest.fixture(scope="module")
async def mock_event() -> AsyncGenerator[List[Event], None]:
  new_event = Event(
    creator="testuser@mail.com",
    title="Event test title",
    image="eventimagetest.png",
    description="Event test description",
    tags=["test_python", "test_book", "test_launch"],
    location="Test Google Meet"
  )

  new_event2 = Event(
    creator="testuser1@mail.com",
    title="Event test title1",
    image="eventimagetest.png",
    description="Event test description1",
    tags=["test_python", "test_book", "test_launch"],
    location="Test Google Meet"
  )
  await Event.insert_one(new_event)
  await Event.insert_one(new_event2)

  yield [new_event, new_event2]


@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient, mock_event: List[Event]) -> None:
  response = await default_client.get("/events/")

  assert response.status_code == 200
  assert response.json()[0]["_id"] == str(mock_event[0].id)


@pytest.mark.asyncio
async def test_get_event(default_client: httpx.AsyncClient, mock_event: List[Event]) -> None:
  url = f"/events/{str(mock_event[0].id)}"
  response = await default_client.get(url)

  assert response.status_code == 200
  assert response.json()["creator"] == mock_event[0].creator
  assert response.json()["_id"] == str(mock_event[0].id)

@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient, access_token: str) -> None:
  payload = {
    "title": "Test event titlte",
    "image": "imagetest.png",
    "description": "Event test description",
    "tags": ["python", "react", "aws"],
    "location": "Google Meet"
  }

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
  }

  test_response = {
    "message": "Event created successfully"
  }

  response = await default_client.post("/events/new", json=payload, headers=headers)

  assert response.status_code == 200
  assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_events_count(default_client: httpx.AsyncClient) -> None:
  response = await default_client.get("/events/")

  events = response.json()

  assert response.status_code == 200
  assert len(events) == 3

@pytest.mark.asyncio
async def test_update_event(default_client: httpx.AsyncClient, mock_event: List[Event], access_token: str) -> None:
  test_payload = {
    "title": "Updated test title for event"
  }

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
  }

  url = f"/events/{str(mock_event[0].id)}"

  response = await default_client.put(url, json=test_payload, headers=headers)

  assert response.status_code == 200
  assert response.json()["title"] == test_payload["title"]

@pytest.mark.asyncio
async def test_delete_event(default_client: httpx.AsyncClient, mock_event: List[Event], access_token: str) -> None:
  test_response = {
    "message": "Event deleted successfully"
  }

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
  }

  url = f"/events/{mock_event[0].id}"

  response = await default_client.delete(url, headers=headers)

  assert response.status_code == 200
  assert response.json() == test_response

async def test_delete_event_failure(default_client: httpx.AsyncClient, mock_event: List[Event], access_token: str) -> None:

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
  }

  url = f"/events/{mock_event[1].id}"

  response = await default_client.delete(url, headers=headers)

  assert response.status_code == 400

async def test_delete_event_failure_not_found(default_client: httpx.AsyncClient, mock_event: List[Event], access_token: str) -> None:

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
  }

  print(mock_event)

  url = f"/events/{mock_event[0].id}"

  response = await default_client.delete(url, headers=headers)

  assert response.status_code == 404