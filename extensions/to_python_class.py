import keyword
import re

from jinja2.ext import Extension


# taken from Django
# https://github.com/django/django/blob/main/django/utils/text.py
def to_python_class(value: str):
    # Split the string by any non-alphanumeric characters.
    tokens = re.split(r"[^0-9a-zA-Z]+", value)
    # Remove any empty tokens that may result from leading/trailing delimiters.
    tokens = [token for token in tokens if token]

    # If there are no valid tokens, return a default class name.
    if not tokens:
        class_name = "Class"
    else:
        # Capitalize each token and join them to form a PascalCase name.
        class_name = "".join(token.capitalize() for token in tokens)

    # If the resulting class name starts with a digit, prefix it with an underscore.
    if class_name and class_name[0].isdigit():
        class_name = "_" + class_name

    # If the class name (in lowercase) is a Python reserved keyword, append 'Class'.
    if class_name.lower() in keyword.kwlist:
        class_name += "Class"

    return class_name


class ToPythonClassExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["to_python_class"] = to_python_class
