from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Union
app = FastAPI()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    # the model_dump on a pydantic object, just converts the model into a dictionary
    # If we take a dict like user_dict and pass it to a function (or class) with **user_dict,
    # Python will "unwrap" it. It will pass the keys and values of the user_dict directly as key-value arguments.
    # UserInDB(**user_dict)
    # would result in something equivalent to:

    # UserInDB(
    #     username="john",
    #     password="secret",
    #     email="john.doe@example.com",
    #     full_name=None,
    # )
    # Or more exactly, using user_dict directly, with whatever contents it might have in the future:

    # UserInDB(
    #     username = user_dict["username"],
    #     password = user_dict["password"],
    #     email = user_dict["email"],
    #     full_name = user_dict["full_name"],
    # )
    user_in_db = UserInDB(**user_in.model_dump(),
                          hashed_password=hashed_password)
    # with the unwrapped dictionary and the extra argument, we have
    # UserInDB(
    # username = user_dict["username"],
    # password = user_dict["password"],
    # email = user_dict["email"],
    # full_name = user_dict["full_name"],
    # hashed_password = hashed_password,
    # )
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


# UNION OF RESPONSE MODELS
class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


# When defining a Union, include the most specific type first, followed by the less specific type.
# In the example below, the more specific PlaneItem comes before CarItem in Union[PlaneItem, CarItem].
# I think what the docs means by specific type is one with more parameters

# In this example we pass Union[PlaneItem, CarItem] as the value of the argument response_model.
# Because we are passing it as a value to an argument instead of putting it in a type annotation, we have to use Union even in Python 3.10.
# So we can't use the vertical bars, as those are for type annotations not arguments
@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

# You can also declare a response using a plain arbitrary dict, declaring just the type of the keys and values, without using a Pydantic model.
# This is useful if you don't know the valid field/attribute names (that would be needed for a Pydantic model) beforehand.


@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
