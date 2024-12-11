from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


# If you declare it as is, because it is a singular value, FastAPI will assume that it is a query parameter.
# But you can instruct FastAPI to treat it as another body key using Body
# fastapi would expect a body that looks like
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}


@app.put("/items1/{item_id}")
async def update_item(*,
                      item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
                      q: str | None = None,
                      item: Item | None = None, user: User, importance: Annotated[int, Body(gt=3)],
                      ):
    results = {"item_id": item_id, "user": user}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# Let's say you only have a single item body parameter from a Pydantic model Item.
# By default, FastAPI will then expect its body directly.
# But if you want it to expect a JSON with a key item and inside of it the model contents,
# as it does when you declare extra body parameters, you can use the special Body parameter embed:
# In this case FastAPI will expect a body like:

{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
# instead of:


{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}


@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
