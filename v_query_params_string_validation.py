from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

# NB that the default value should obey the rules provided in the Query function.


# If you define an endpoint like @app.get("/items0/"), both /items0/ and /items0 will redirect to /items0/.
# Similarly, if you define an endpoint like @app.get("/items0"), both /items0 and /items0/ will redirect to /items0.
# To change this behaviour - app = FastAPI(redirect_slashes=False)


@app.get("/items0")
async def read_items(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# having Query(max_length=50) inside of Annotated,
# we are telling FastAPI that we want it to have additional validation for this value, we want it to have maximum 50 characters.
# using annotated is advised

# I think the reason why using annotated is advised is because if you wanted to use the function particularly if the function parameters
# were not optional, using Query, you won't get any editor highlighting of errors if you don't provide a value for that parameter,
# as its value is already Query. But with Annotated, you are not providing a default value for the function parameter, all you're doing is
# just giving a type hint that fastapi uses


@app.get("/items1/")
async def read_items(q: Annotated[str | None, Query(max_length=50, min_length=4)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# The ellipsis as the default value of b makes it a required query parameter
# So this didn't work for me. It resulted to an internal server error when the query parameter q wasn't provided.
# So, in a way you can say it works, only that it crashes your server


@app.get("/items2")
async def read_items(q: Annotated[str, Query(max_length=10)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# So the solution to the error from the above endpoint is
# TODO Fix this in the docs
# Sha the best way to make a parameter required is by not providing a default value for it
@app.get("/items3")
async def read_items(q: Annotated[str, Query(max_length=10, default=...)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# When you define a query parameter explicitly with Query you can also declare it to receive a list of values,
# or said in another way, to receive multiple values.

# For example, to declare a query parameter q that can appear multiple times in the URL, you can write:@app.get("/items/")
# URL would look like http://localhost:8000/items/?q=foo&q=bar

@app.get(path="/items4")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items


class Foo:
    pass

# fastapi just converts the default values to String, if they are convertible, else you get a 422 validation error
# if no value is provided


@app.get(path="/items5")
async def read_items(q: Annotated[list[str] | None, Query()] = [[], False, Foo()]):
    query_items = {"q": q}
    return query_items

# adding more metadata
# NB that the default value should obey the rules provided in the Query function.
# For instance in item6 endpoint, if I made the default value a list of 2 items when the min_length should be 3
# this would lead to a 422 validation error


@app.get(path="/items6")
async def read_items(q: Annotated[list[str], Query(title="Query string",
                                                   description="Query string for the items to search in the database that have a good match", min_length=3,
                                                   ),] = ["fo", "bar", "boo"],):
    query_items = {"q": q}
    return query_items


# Imagine that you want the parameter to be item-query.

# Like in: http://127.0.0.1:8000/items/?item-query=foobaritems
# But item-query is not a valid Python variable name.

# The closest would be item_query.

# But you still need it to be exactly item-query...

# Then you can declare an alias, and that alias is what will be used to find the parameter value:
@app.get("/items7")
async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# to indicate that a parameter is now deprecated
# you don't want to just remove it because some clients could still be using it.
# But you just want to be able to indicate to already existing clients and even new clients that this parameter
# is now deprecated
@app.get("/items8")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# To exclude a query parameter from the generated OpenAPI schema (and thus, from the automatic documentation systems),
# set the parameter include_in_schema of Query to False:


@app.get("/items9")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}
