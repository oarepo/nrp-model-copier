import sys


def register_model_to_invenio_cfg(model_name, endpoint):

    invenio_cfg_path = "invenio.cfg"
    model_registration = f"""
# {model_name} model registration
from models.{model_name} import {model_name}_model
# TODO: remove this once everyone is migrated to oarepo-ui >=7
{model_name}_model.register()
DASHBOARD_RECORD_CREATE_URL = "/{endpoint}/uploads/new"
"""

    with open(invenio_cfg_path, "a") as invenio_cfg:
        invenio_cfg.write(model_registration)


if __name__ == "__main__":
    register_model_to_invenio_cfg(sys.argv[1], sys.argv[2])
