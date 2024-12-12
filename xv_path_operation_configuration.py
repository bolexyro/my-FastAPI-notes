from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

# based on what I've seen, tags are just supposed to kinda group your endpoints in the automatic documentation


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]

# You could also use enums
# Using enums could be better than using strings because you could have typos when writing the string
# and enums give you editor support


class Tags(Enum):
    items = "items"
    users = "users"


@app.get("/users2/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]


# summary and description are self explanatory
# They give you a summary and description of an endpoint in the documentations
# The default summary is just the name of the function without underscore and .capitalized
@app.post(
    "/items1/",
    response_model=Item,
    tags=[Tags.users, Tags.items],
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item


# As descriptions tend to be long and cover multiple lines,
# you can declare the path operation description in the function docstring and FastAPI will read it from there.
# You can write Markdown in the docstring, it will be interpreted and displayed correctly (taking into account docstring indentation).
# You can specify the response description with the parameter response_description:


@app.post("/items2/", response_model=Item, summary="Create an item", response_description="The created item ")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# If you need to mark a path operation as deprecated, but without removing it, pass the parameter deprecated:
# in the docs, it is greyed out and striked out


@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
