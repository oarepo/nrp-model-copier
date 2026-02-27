"""Copy variant-specific files over the base template with Jinja processing."""

import sys
from pathlib import Path

import yaml
from jinja2 import Environment, BaseLoader

from slugify import slugify
from to_python_class import to_python_class


class StringLoader(BaseLoader):
    """Loader that loads templates from strings."""

    def get_source(self, environment, template):
        return template, None, lambda: True


def create_jinja_env():
    """Create Jinja environment with custom filters."""
    env = Environment(loader=StringLoader())
    env.filters["slugify"] = slugify
    env.filters["to_python_class"] = to_python_class
    return env


def load_variables(model_name: str) -> dict:
    """Load variables from .copier-answers.yml file."""
    answers_file = Path.cwd() / model_name / ".copier-answers.yml"
    if answers_file.exists():
        with open(answers_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            # Remove copier internal keys (start with _)
            return {k: v for k, v in data.items() if not k.startswith("_")}
    return {}


def copy_variant(base_model: str, model_name: str, src_path: str) -> None:
    """Copy variant files to destination with Jinja processing."""
    variant_dir = Path(src_path) / "template" / "_variants" / base_model

    if not variant_dir.exists():
        print(f"Warning: Variant directory not found: {variant_dir}")
        return

    # Current directory is the destination (where copier runs)
    dest_dir = Path.cwd()

    # Load variables from answers file
    variables = load_variables(model_name)
    print(f"Loaded variables: {list(variables.keys())}")

    # Create Jinja environment
    jinja_env = create_jinja_env()

    # Walk through variant files and copy them
    for src_file in variant_dir.rglob("*"):
        if src_file.is_file():
            # Get relative path from variant dir
            rel_path = src_file.relative_to(variant_dir)

            # Replace {{model_name}} in path with actual model_name
            rel_path_str = str(rel_path).replace("{{model_name}}", model_name)

            # Strip .copier suffix if present
            if rel_path_str.endswith(".copier"):
                rel_path_str = rel_path_str[:-7]

            dest_file = dest_dir / rel_path_str

            # Create parent directories if needed
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Read source file
            content = src_file.read_text(encoding="utf-8")

            # Process Jinja templates for .copier files (and other template files)
            if src_file.suffix == ".copier" or "{{" in content:
                try:
                    template = jinja_env.from_string(content)
                    content = template.render(**variables)
                except Exception as e:
                    print(f"Warning: Failed to process template {rel_path}: {e}")

            # Write to destination
            dest_file.write_text(content, encoding="utf-8")
            print(f"Copied variant file: {rel_path_str}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: copy_variant.py <base_model> <model_name> <src_path>")
        sys.exit(1)

    copy_variant(sys.argv[1], sys.argv[2], sys.argv[3])
