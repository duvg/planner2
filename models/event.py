from pydantic import BaseModel
from beanie import Document
from typing import List, Optional

class Event(Document):
  title: str
  image: str
  description: str
  tags: List[str]
  location: str
  creator: Optional[str]

  class Config:
    json_schema_extra = {
      "example": {
        "title": "Event Planner API",
        "image": "https://cdn.pixabay.com/photo/2017/04/25/22/28/despaired-2261021_1280.jpg",
        "description": "Example of event planner",
        "tags": ["python", "fastapi", "rest"],
        "location": "Google Meet"
      }
    }

  class Settings:
    name = "events"

class EventUpdate(BaseModel):
  title: Optional[str]
  image: Optional[str]
  description: Optional[str]
  tags: Optional[List[str]]
  location: Optional[str]

  class Config:
    json_schema_extra = {
      "example": {
        "title": "Event lanner title to update",
        "image": "https://cdn.pixabay.com/photo/2017/04/25/22/28/despaired-2261021_1280.jpg",
        "tags": ["python", "fastapi", "mongodb"],
        "location": "Google Meet"
      }
    }
