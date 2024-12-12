from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


app = FastAPI()

# jsonable_encoder receives an object, like a Pydantic model, and returns a JSON compatible version:
# In this example, it would convert the Pydantic model to a dict, and the datetime to a str.
# it doesn't return a json string, nope it returns a python object - dict that is json compatible
# so you could do json.dumps on the resulting dict to get the json string


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
