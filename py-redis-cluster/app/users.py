# @klotho::execution_unit {
#  id = "users"
# }
import logging

from fastapi import FastAPI
from starlette.responses import PlainTextResponse
from pydantic import BaseModel

from my_redis import client

# @klotho::expose {
#   id = "users-gw"
#   target = "public"
# }
app = FastAPI()

@app.get("/users/{name}", response_class=PlainTextResponse)
async def get_user(name: str):
  logging.info(name)
  user = client.get(f"user/{name}")
  return user

class User(BaseModel):
  first_name: str
  last_name: str

@app.put("/users", response_class=PlainTextResponse)
async def add_users(user: User):
  logging.info(user)
  client.set(f"user/{user.first_name}", user.last_name)
  return "Success"


