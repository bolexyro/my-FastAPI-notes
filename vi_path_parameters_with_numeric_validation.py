from fastapi import FastAPI, Path, Query
from typing import Annotated

app = FastAPI()

# A path parameter is always required as it has to be part of the path.
# Even if you declared it with None or set a default value, it would not affect anything, it would still be always required.


@app.get("/items1/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# Order the parameters as you need¶
@app.get("/items2/{item_id}")
# async def read_items(item_id: int = Path(title="The ID of the item to get"), q: str):   This would give an error - Non-default argument follows default argument
# so to prevent this you could just reorder them as the order doesn't matter
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Anothe rwy to prevent this is to use annotated


@app.get("/items3/{item_id}")
async def read_items(
    q: str, item_id: Annotated[int, Path(title="The ID of the item to get")]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# another way around this
# Python won't do anything with that *,
# but it will know that all the following parameters should be called as keyword arguments (key-value pairs),
# also known as kwargs. Even if they don't have a default value.
@app.get("/items4/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# NB: If you use annotated, you won't have this problem sha


# Number validations
# ge = greater than or equal to
# gt = greater than
# le = less than or equal to
# lt = less than
@app.get("/items5/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
