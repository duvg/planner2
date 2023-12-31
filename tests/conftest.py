import asyncio
import pytest_asyncio

import httpx
import pytest

from database.connection import Settings
from main import app
from models.event import Event
from models.user import User

@pytest.fixture(scope="session")
def event_loop():
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  yield loop
  loop.close()

async def init_db():
  test_settings = Settings()
  test_settings.DATABASE_URL = "mongodb://localhost:27017/testdb"

  await test_settings.initialize_database()


@pytest_asyncio.fixture(scope="session")
async def default_client():
  await init_db()
  async with httpx.AsyncClient(app=app, base_url="http://app") as client:
    yield client
    # Clean up resources
    await Event.find_all().delete()
    await User.find_all().delete()

