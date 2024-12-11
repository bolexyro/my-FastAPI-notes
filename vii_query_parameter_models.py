from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# If you have a group of query parameters that are related, you can create a Pydantic model to declare them.

# This would allow you to re-use the model in multiple places and also to declare validations and metadata for all the parameters at once. 😎


class FilterParams(BaseModel):
    # You can use Pydantic's model configuration to forbid any extra fields:
    # like if you don't want them to include a parameter you haven't defined
    # if the client does, they receive a 422 error with a message "Extra inputs are not permitted"
    model_config = {"extra": "forbid"}
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

# An example of a url for this would be http://localhost:8000/items/?limit=100&offset=0&order_by=created_at&tags=string&tags=string

# FastAPI will extract the data for each field from the query parameters in the request and give you the Pydantic model you defined


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
