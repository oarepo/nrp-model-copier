import sys

SIDEBAR_BOXES = {
    "empty": ["export", "citations", "technical_metadata"],
    "rdm_basic": ["manage_menu", "communities", "export", "citations", "technical_metadata"],
    "rdm_minimal": ["manage_menu", "communities", "export", "citations", "technical_metadata"],
    # "ccmm" is the default, no modifications here
}


def register_model_to_invenio_cfg(model_name, base_model=None):

    invenio_cfg_path = "invenio.cfg"
    marker = f"# {model_name} model registration"
    model_registration = f"""
{marker}
from models.{model_name} import {model_name}_model

{model_name}_model.register()
"""

    # Record detail sidebar of the model: box name lists per preset, see
    # oarepo_config.detail_sidebar.DETAIL_SIDEBAR_TEMPLATES for the known boxes.
    # rdm_complete uses the default sidebar set by configure_ui.
    if base_model == "ccmm":
        # ccmm-invenio provides a sidebar box with a map of the record's geographic locations
        model_registration += f"""
config.configure_detail_sidebar(
    model="{model_name}",
    templates={{
        "locations": "ccmm_invenio/record_detail/side_bar/locations.html",
    }},
    move=["locations after details"],
)
"""
    elif base_model in SIDEBAR_BOXES:
        boxes = ",\n".join(f'        "{box}"' for box in SIDEBAR_BOXES[base_model])
        model_registration += f"""
config.configure_detail_sidebar(
    model="{model_name}",
    # only these boxes, in this order
    order=[
{boxes},
    ],
)
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
    register_model_to_invenio_cfg(*sys.argv[1:3])
