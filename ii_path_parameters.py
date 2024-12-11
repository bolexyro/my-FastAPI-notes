from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# "Path" here refers to the last part of the URL starting from the first /.
# So, in a URL like: https://example.com/items/foo
# the path would be: /items/foo

# A "path" is also commonly called an "endpoint" or a "route".

# Normally you use HTTP methods:
# POST: to create data.
# GET: to read data.
# PUT: to update data.
# DELETE: to delete data.

# The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:
# the path /
# using a get operation


@app.get(path='/')
def root():
    return 'Hi There'

# You can declare path "parameters" or "variables" with the same syntax used by Python format strings

# As they are part of the URL, they are "naturally" strings.
# But when you declare them with Python types (in the example below, as int), they are converted to that type and validated against it.


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# If you have a path operation that receives a path parameter,
# but you want the possible valid path parameter values to be predefined, you can use a standard Python Enum.


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
