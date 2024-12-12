# You can declare the type used for the response by annotating the path operation function return type.

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Any
from fastapi.responses import JSONResponse, RedirectResponse, Response

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]

# FastAPI will use this return type to:

# 1. Validate the returned data. If the data is invalid
# (e.g. you are missing a field), it means that your app code is broken,
# not returning what it should, and it will return a server error instead of returning incorrect data.
# This way you and your clients can be certain that they will receive the data and the data shape expected.
# 2. Add a JSON Schema for the response, in the OpenAPI path operation. This will be used by the automatic docs.
# It will also be used by automatic client code generation tools.
# But most importantly:

# 3. It will limit and filter the output data to what is defined in the return type.
# This is particularly important for security, we'll see more of that below.


# In a case where you want to return some data that is not exactly what the type declares
# For example, you could want to return a dictionary or a database object, but declare it as a Pydantic model.
# This way the Pydantic model would do all the data documentation, validation, etc.
# for the object that you returned (e.g. a dictionary or database object).

# If you added the return type annotation, tools and editors would complain with a
# (correct) error telling you that your function is returning a type (e.g. a dict) that is different from what you declared (e.g. a Pydantic model).

# a work around for this issue is to use the response_model as shown below
# FastAPI will use this response_model to do all the data documentation, validation, etc.
# and also to convert and filter the output data to its type declaration

# If you declare both a return type and a response_model, the response_model will take priority and be used by FastAPI.
# This way you can add correct type annotations to your functions even when you are returning a type different than the response model,
# to be used by the editor and tools like mypy. And still you can have FastAPI do the data validation, documentation, etc. using the response_model.

@app.post("/items2/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items2/", response_model=list[Item])
async def read_items() -> list[dict]:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user

# Here, even though our path operation function is returning the same input user that contains the password,
# we declared the response_model to be our model UserOut, that doesn't include the password:

# So, FastAPI will take care of filtering out all the data that is not declared in the output model (using Pydantic).
# In this case, because the two models are different, if we annotated the function return type as UserOut,
# the editor and tools would complain that we are returning an invalid type, as those are different classes.
# That's why in this example we have to declare it in the response_model parameter.


# using response_model means that we don't get the support from the editor and tools checking the function return type.
# But in most of the cases where we need to do something like this, we want the model just to filter/remove some of the data as in the example above
# And in those cases, we can use classes and inheritance to take advantage of function type annotations
# to get better support in the editor and tools, and still get the FastAPI data filtering.


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


# With this, we get tooling support,
# from editors and mypy as this code is correct in terms of types, but we also get the data filtering from FastAPI.
@app.post("/user2/")
async def create_user(user: UserIn) -> BaseUser:
    return user


# The reasoning behind it
# BaseUser has the base fields. Then UserIn inherits from BaseUser and adds the password field,
# so, it will include all the fields from both models.

# We annotate the function return type as BaseUser, but we are actually returning a UserIn instance.

# The editor, mypy, and other tools won't complain about this because, in typing
# terms, UserIn is a subclass of BaseUser, which means it's a valid type when what is expected is anything that is a BaseUser.
# Now, for FastAPI, it will see the return type and make sure that what you return includes only the fields that are declared in the type.


# Other types of response
# Suppose you want to return something that is not a pydantic model
# tools will also be happy because both RedirectResponse and JSONResponse are subclasses of Response, so the type annotation is correct.
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


# .this fails because the type annotation is not a Pydantic type and is not just a single Response class or subclass, it's a union (any of the two) between a Response and a dict.
# @app.get("/mkbhd")
# async def get_portal(teleport: bool = False) -> dict | Response:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return {"message": "Here's your interdimensional portal."}

# to make it work, set response_model to None
@app.get("/mkbhd", response_model=None)
async def get_portal(teleport: bool = False) -> dict | Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}


class Item2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


# if you have models with many optional attributes in for example a NoSQL database,
# but you don't want to send very long JSON responses full of default values.
# You can also use:

# response_model_exclude_defaults=True
# response_model_exclude_none=True
@app.get("/items3/{item_id}", response_model=Item2, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]

# those default values won't be included in the response, only the values actually set.
# So, if you send a request to that path operation for the item with ID foo, the response (not including default values) will be:

{
    "name": "Foo",
    "price": 50.2
}
# But if your data has values for the model's fields with default values, like the item with ID bar:


{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}
# they will be included in the response.
# If the data has the same values as the default ones, like the item with ID baz:


{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
# FastAPI is smart enough (actually, Pydantic is smart enough) to realize that,
# even though description, tax, and tags have the same values as the defaults,
# they were set explicitly (instead of taken from the defaults).

# So, they will be included in the JSON response.

# response_model_include and response_model_exclude¶
# You can also use the path operation decorator parameters response_model_include and response_model_exclude.
# They take a set of str with the name of the attributes to include (omitting the rest) or to exclude (including the rest).
# This can be used as a quick shortcut if you have only one Pydantic model and want to remove some data from the output.


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]


# But it is still recommended to use the ideas above, using multiple classes, instead of these parameters.
# This is because the JSON Schema generated in your app's OpenAPI (and the docs)
#  will still be the one for the complete model, even if you use response_model_include or response_model_exclude to omit some attributes.

# This also applies to response_model_by_alias that works similarly.

# If you forget to use a set and use a list or tuple instead for the inclue or exclude, FastAPI will still convert it to a set and it will work correctly:
