# A request body is data sent by the client to your API. A response body is the data your API sends to the client.
# clients don't always have to send a request body tho. Sometimes, they only request a path, maybe with some query parameters, but don't send a body.

# you use pydantic to declare a request body

from fastapi import FastAPI
from pydantic import BaseModel

# The JSON Schemas of your models will be part of your OpenAPI generated schema, and will be shown in the interactive API docs:


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    # TODO Fix this in docs. Change dict() to model_dump()
    # item_dict = item.dict()
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
