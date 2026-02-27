"""Copy variant-specific files over the base template."""

import shutil
import sys
from pathlib import Path


def copy_variant(base_model: str, model_name: str, src_path: str) -> None:
    """Copy variant files to destination, overwriting base files."""
    variant_dir = Path(src_path) / "template" / "_variants" / base_model

    if not variant_dir.exists():
        print(f"Warning: Variant directory not found: {variant_dir}")
        return

    # Current directory is the destination (where copier runs)
    dest_dir = Path.cwd()

    # Walk through variant files and copy them
    for src_file in variant_dir.rglob("*"):
        if src_file.is_file():
            # Get relative path from variant dir
            rel_path = src_file.relative_to(variant_dir)

            # Replace {{model_name}} in path with actual model_name
            rel_path_str = str(rel_path).replace("{{model_name}}", model_name)
            dest_file = dest_dir / rel_path_str

            # Create parent directories if needed
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Copy file (overwrite if exists)
            shutil.copy2(src_file, dest_file)
            print(f"Copied variant file: {rel_path_str}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: copy_variant.py <base_model> <model_name> <src_path>")
        sys.exit(1)

    copy_variant(sys.argv[1], sys.argv[2], sys.argv[3])
