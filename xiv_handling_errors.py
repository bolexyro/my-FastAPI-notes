# To return HTTP responses with errors to the client you use HTTPException.
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi import FastAPI, HTTPException, Request, Path
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from typing import Annotated

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: Annotated[int, Path(gt=2)]):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "There goes my error"},
                            )
    return {"item": items[item_id]}

# Let's say you have a custom exception UnicornException that you (or a library you use) might raise.
# And you want to handle this exception globally with FastAPI.
# You could add a custom exception handler with @app.exception_handler():


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        # Here, if you request /unicorns/yolo, the path operation will raise a UnicornException.
        # But it will be handled by the unicorn_exception_handler.
        # and a 418 error will be returned rather than a 500 if the exception handler weren't there
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# FastAPI has some default exception handlers.
# These handlers are in charge of returning the default JSON responses when you raise an HTTPException and when the request has invalid data.
# You can override these exception handlers with your own.
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return PlainTextResponse(str(exc.detail) + " mkbhd is da goat", status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(str(exc) + " mkbhd is a legend", status_code=400)


# So the difference betwee fastapi's httpexception and starlette's httpexception is that the details field in fastapi's accepts
# any jsonable data, while the one in starlette's httpexception only takes string.

# FastAPI's HTTPException error class inherits from Starlette's HTTPException error class.
# when you register an exception handler, it is best to register it for starlette's httpexception.
# This way, if any part of Starlette's internal code, or a Starlette extension or plug-in,
# raises a Starlette HTTPException, your handler will be able to catch and handle it.


# if you want to reuse the default exception handlers from fastapi


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler2(request: Request, exc: StarletteHTTPException):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)
