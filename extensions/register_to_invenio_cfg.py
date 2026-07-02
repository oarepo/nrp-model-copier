import sys


def register_model_to_invenio_cfg(model_name):

    invenio_cfg_path = "invenio.cfg"
    marker = f"# {model_name} model registration"
    model_registration = f"""
{marker}
from models.{model_name} import {model_name}_model

{model_name}_model.register()
"""

    try:
        with open(invenio_cfg_path, "r") as invenio_cfg:
            if marker in invenio_cfg.read():
                return
    except FileNotFoundError:
        pass

    with open(invenio_cfg_path, "a") as invenio_cfg:
        invenio_cfg.write(model_registration)


if __name__ == "__main__":
    register_model_to_invenio_cfg(sys.argv[1])
