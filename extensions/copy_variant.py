"""Copy variant-specific files using Copier's built-in rendering."""

import sys
from pathlib import Path

import yaml
from copier import run_copy


def copy_variant(base_model: str, model_name: str, src_path: str) -> None:
    """Copy variant files to destination using Copier."""
    variant_dir = Path(src_path) / "template" / "_variants" / base_model

    if not variant_dir.exists():
        print(f"Warning: Variant directory not found: {variant_dir}")
        return

    # Current directory is the destination
    dest_dir = Path.cwd()

    # Load answers from the already-created answers file
    answers_file = dest_dir / model_name / ".copier-answers.yml"

    if not answers_file.exists():
        print(f"Warning: Answers file not found at {answers_file}")
        return

    # Load the data from answers file
    with open(answers_file, "r", encoding="utf-8") as f:
        answers = yaml.safe_load(f)

    # Filter out internal copier keys and prepare data
    data = {k: v for k, v in answers.items() if not k.startswith("_")}

    print(f"Copying variant '{base_model}' using Copier...")
    print(f"Source: {variant_dir}")
    print(f"Destination: {dest_dir}")
    print(f"Data: {data}")

    # Use Copier to copy the variant, reusing all its template processing
    run_copy(
        src_path=str(variant_dir),
        dst_path=str(dest_dir),
        data=data,
        unsafe=True,
        defaults=True,
        overwrite=True,
    )

    print(f"Variant '{base_model}' copied successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: copy_variant.py <base_model> <model_name> <src_path>")
        sys.exit(1)

    copy_variant(sys.argv[1], sys.argv[2], sys.argv[3])
