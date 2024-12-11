def get_full_name(first_name: str, last_name: str) -> str:
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name("john", "doe"))


def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age


print(get_name_with_age(name='Bolexyro', age=19))


def say_hi(name: str | None = ''):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")

say_hi()


# type hints with metadata annotations
from typing import Annotated
# The important thing to remember is that the first type parameter you pass to Annotated is the actual type.
# The rest, is just metadata for other tools.
def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
    return f"Hello {name}"