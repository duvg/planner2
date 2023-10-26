from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.event import Event

class User(Document):
  email: EmailStr
  password: str
  events: Optional[List[Link[Event]]]

  class Settings:
    name = "users"

  class Config:
    json_schema_extra = {
      "example": {
        "email": "user@mail.com",
        "username": "theusername",
        "events": [],
      }
    }

class TokenResponse(BaseModel):
  access_token: str
  token_type: str

  class Config:
    json_schema_extra = {
      "example": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidXNlcjFAbWFpbC5jb20iLCJleHBpcmVzIjoxNjk2MTE1NzAwLjMzNzg4MX0.eJyZzDExjS1R4GCOSu5J5JQWgc7yJnisAWoGWY9B3uU",
        "token_type": "Bearer",
        "events": [],
      }
    }