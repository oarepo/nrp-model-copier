"""Copy variant-specific files with Jinja processing."""

import sys
from pathlib import Path

import yaml
from jinja2 import Environment, BaseLoader

# Import filter functions directly (same directory)
sys.path.insert(0, str(Path(__file__).parent))
from slugify import slugify
from to_python_class import to_python_class


def create_jinja_env():
    """Create Jinja environment with custom filters."""
    env = Environment(
        loader=BaseLoader(),
        keep_trailing_newline=True,
    )
    env.filters["slugify"] = slugify
    env.filters["to_python_class"] = to_python_class
    return env


def copy_variant(base_model: str, model_name: str, src_path: str) -> None:
    """Copy variant files to destination with Jinja processing."""
    variant_dir = Path(src_path) / "template" / "_variants" / base_model
    dest_dir = Path.cwd()
    answers_file = dest_dir / model_name / ".copier-answers.yml"

    print(f"=== copy_variant ===")
    print(f"base_model: {base_model}")
    print(f"model_name: {model_name}")
    print(f"variant_dir: {variant_dir}")
    print(f"dest_dir: {dest_dir}")
    print(f"answers_file: {answers_file}")

    if not variant_dir.exists():
        print(f"ERROR: Variant directory not found: {variant_dir}")
        return

    if not answers_file.exists():
        print(f"ERROR: Answers file not found: {answers_file}")
        return

    # Load variables
    with open(answers_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    variables = {k: v for k, v in data.items() if not k.startswith("_")}
    print(f"Variables: {variables}")

    jinja_env = create_jinja_env()

    # Process all files in variant directory (skip copier.yml)
    for src_file in variant_dir.rglob("*"):
        if src_file.is_file() and src_file.name != "copier.yml":
            rel_path = src_file.relative_to(variant_dir)

            # Render path (replace {{model_name}} in directory/file names)
            rel_path_str = str(rel_path)
            try:
                rel_path_str = jinja_env.from_string(rel_path_str).render(**variables)
            except Exception as e:
                print(f"Warning: Failed to render path {rel_path}: {e}")

            # Strip .copier suffix
            if rel_path_str.endswith(".copier"):
                rel_path_str = rel_path_str[:-7]

            dest_file = dest_dir / rel_path_str
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Read and process content
            content = src_file.read_text(encoding="utf-8")

            if src_file.suffix == ".copier" or "{{" in content:
                try:
                    content = jinja_env.from_string(content).render(**variables)
                except Exception as e:
                    print(f"ERROR processing {rel_path}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue

            dest_file.write_text(content, encoding="utf-8")
            print(f"Copied: {rel_path_str}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: copy_variant.py <base_model> <model_name> <src_path>")
        sys.exit(1)

    copy_variant(sys.argv[1], sys.argv[2], sys.argv[3])
