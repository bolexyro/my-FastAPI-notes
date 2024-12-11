from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None
    images: list[Image] | None = None


# This will expect (convert, validate, document, etc.) a JSON body like:
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    },
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

# If the top level value of the JSON body you expect is a JSON array
# (a Python list), you can declare the type in the parameter of the function, the same as in Pydantic models:


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images

# Bodies of arbitrary dicts¶
# You can also declare a body as a dict with keys of some type and values of some other type.
# This way, you don't have to know beforehand what the valid field/attribute names are (as would be the case with Pydantic models).
# This would be useful if you want to receive keys that you don't already know.
# Another useful case is when you want to have keys of another type (e.g., int).
# That's what we are going to see here.
# In this case, you would accept any dict as long as it has int keys with float values:

# Keep in mind that JSON only supports str as keys.
# But Pydantic has automatic data conversion.
# This means that, even though your API clients can only send strings as keys, as long as those strings contain pure integers, Pydantic will convert them and validate them.
# And the dict you receive as weights will actually have int keys and float values.


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights
