# @klotho::execution_unit {
#  id = "quotes"
# }
import logging

from fastapi import FastAPI
from starlette.responses import PlainTextResponse
from pydantic import BaseModel

from app.my_redis import client

# @klotho::expose {
#   id = "quotes-gw"
#   target = "public"
# }
app = FastAPI()

@app.get("/quote", response_class=PlainTextResponse)
async def get_quote():
  quote = client.get("quote")
  return quote

class Quote(BaseModel):
  quote: str

@app.put("/quote", response_class=PlainTextResponse)
async def set_quote(quote: Quote):
  logging.info(quote)
  client.set("quote", quote.quote)
  return "Success"


