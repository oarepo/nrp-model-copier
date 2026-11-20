"""An extension that registers the model to the pyproject.toml file."""

import re
import sys

# tomlkit preserves comments and formatting of the user's pyproject.toml
import tomlkit


class PyProject:
    def __init__(self, path):
        self.pyproject_file = path
        with open(self.pyproject_file, "r", encoding="utf-8") as f:
            self.pyproject_data = tomlkit.load(f)

    def save(self):
        with open(self.pyproject_file, "w", encoding="utf-8") as f:
            tomlkit.dump(self.pyproject_data, f)

    def add_dependencies(self, *dependencies):
        self.update_dependencies_array(
            self.pyproject_data["project"].setdefault("dependencies", []), dependencies
        )
        return self

    def add_optional_dependencies(self, group, *dependencies):
        self.update_dependencies_array(
            self.pyproject_data["project"]
            .setdefault("optional-dependencies", {})
            .setdefault(group, []),
            dependencies,
        )
        return self

    def add_entry_point(self, group, name, value):
        toml_entry_points = self.pyproject_data["project"].setdefault(
            "entry-points", {}
        )

        if group in toml_entry_points:
            toml_entry_points[group][name] = value
        else:
            ep_group = tomlkit.table()
            ep_group[name] = value
            ep_group.add(tomlkit.nl())  # blank line before the next table
            toml_entry_points[group] = ep_group
        return self

    def update_dependencies_array(self, target_array, new_values):
        target_packages = [re.split("[<>=]", ta)[0] for ta in target_array]
        for value in new_values:
            if not value:
                continue
            value_package = re.split("[<>=]", value)[0]
            if value_package not in target_packages:
                target_array.append(value)
        target_array.sort()
        return target_array

    def add_top_level_module(self, module_name):
        build_backend = self.pyproject_data["tool"]["uv"]["build-backend"]
        top_level_modules = build_backend.setdefault("module-name", [])

        if module_name not in top_level_modules:
            top_level_modules.append(module_name)


def register_model_to_pyproject(model_name, base_model):
    pyproject = PyProject("pyproject.toml")

    # ensure the models top-level package is included in the build-backend configuration
    pyproject.add_top_level_module("models")

    # add blueprint
    pyproject.add_entry_point(
        "invenio_base.blueprints",
        f"ui_{model_name}",
        f"ui.{model_name}:create_blueprint",
    )

    # add webpack
    pyproject.add_entry_point(
        "invenio_assets.webpack",
        f"ui_{model_name}",
        f"ui.{model_name}.webpack:theme",
    )

    # add finalizers
    pyproject.add_entry_point(
        "invenio_base.finalize_app",
        f"ui_{model_name}",
        f"ui.{model_name}:finalize_app",
    )

    pyproject.save()


if __name__ == "__main__":
    register_model_to_pyproject(sys.argv[1], sys.argv[2])
