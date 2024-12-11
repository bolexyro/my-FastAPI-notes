# When you declare other function parameters that are not part of the path parameters,
# they are automatically interpreted as "query" parameters.

# The query is the set of key-value pairs that go after the ? in a URL, separated by & characters.

from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


# your query parameters could either be required (like skip below) or optional (like limit below)
@app.get("/items/")
async def read_item(skip: int, limit: int = 10):
    return fake_items_db[skip: skip + limit]
