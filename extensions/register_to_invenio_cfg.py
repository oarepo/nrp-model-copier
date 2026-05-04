import sys


def register_model_to_invenio_cfg(model_name):

    invenio_cfg_path = "invenio.cfg"
    model_registration = f"""
# {model_name} model registration
from models.{model_name} import {model_name}_model
{model_name}_model.register()
"""

    with open(invenio_cfg_path, "a") as invenio_cfg:
        invenio_cfg.write(model_registration)


if __name__ == "__main__":
    register_model_to_invenio_cfg(sys.argv[1])
