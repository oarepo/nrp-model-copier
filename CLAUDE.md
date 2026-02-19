# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a **Copier template** for generating new model packages inside the Czech National Repository Platform (NRP). It generates Invenio RDM-compatible models with UI components. The template is not used directly; it's invoked via `nrp-devtools` when creating new repositories.

## Architecture

### Template Structure

```
copier.yml                 # Template configuration and prompts
extensions/                # Jinja2/Context extensions
├── slugify.py            # Adds `slugify` filter for URL-safe names
├── to_python_class.py    # Adds `to_python_class` filter for PascalCase conversion
├── register_to_invenio_cfg.py   # Post-task: registers model in invenio.cfg
└── register_to_pyproject.py    # Post-task: registers model in pyproject.toml
template/                  # The actual template files
├── {{model_name}}/       # Generated Python model package
│   ├── __init__.py
│   ├── model.py          # OARepo model definition with presets
│   ├── metadata.yaml     # Metadata schema definition
│   └── serializers.py
└── ui/{{model_name}}/    # Generated UI package
    ├── __init__.py       # Resource config, blueprint, menu registration
    ├── webpack.py        # Webpack bundle configuration
    ├── semantic-ui/js/   # React components
    └── templates/        # Jinja2 templates
```

### Copier Configuration (`copier.yml`)

Key variables:
- `model_name`: Short identifier (e.g., `datasets`, `theses`)
- `model_human_name`: Human-readable name with default `{{model_name|replace('_', '-')|title}}`
- `base_model`: Choice of preset - `ccmm`, `rdm_complete`, `rdm_basic`, `rdm_minimal`, or `empty`
- `endpoint`: Auto-generated URL slug via `{{ model_name|slugify }}`
- `resource_config` / `resource`: Auto-generated class names via `to_python_class` filter

Template processing:
- Files use `.copier` suffix which gets stripped during generation
- `_templates_suffix: .copier` in config
- `_subdirectory: template` - actual template files are nested under `template/`

### Jinja2 Extensions

Extensions in the `extensions/` directory provide template filters:

1. **slugify**: Converts strings to URL-safe slugs (e.g., `my_model` → `my-model`)
2. **to_python_class**: Converts strings to PascalCase class names (e.g., `my_model` → `MyModel`)

These are registered via `_jinja_extensions` in `copier.yml`.

### Generated Model Architecture

The generated model follows the OARepo/Invenio RDM pattern:

**Model Definition** (`model.py`):
- Uses `oarepo_model.api.model()` decorator
- Supports base presets: `rdm_complete_preset`, `rdm_basic_preset`, `rdm_minimal_preset`, `ccmm_production_preset_1_1_0`, or `records_resources_preset`
- Metadata defined in separate `metadata.yaml` (loaded via `from_yaml()`)
- Customizations via mixins and export extensions
- Permission policy mixin with `can_view_deposit_page`

**UI Resources** (`ui/{{model_name}}/__init__.py`):
- Extends `RecordsUIResourceConfig` and `RecordsUIResource`
- Configures search component pointing to React component path
- Registers blueprint, menu items, and UI overrides
- Includes component imports from `oarepo_ui` (Babel, Files, Permissions, etc.)

**Templates**:
- Extend base `oarepo_ui` templates
- Partial templates for customization: `banners.html`, `main.html`, `javascript.html`
- Template inheritance chain: model template → `oarepo_ui/*` → `invenio_app_rdm/*`

**Post-Generation Tasks** (run automatically by copier):
1. `register_to_pyproject.py`: Adds entry points for blueprints, webpack, finalize_app
2. `register_to_invenio_cfg.py`: Appends model registration code to `invenio.cfg`

## Development Workflow

### Testing the Template

To test template changes locally:

```bash
# Create a temporary directory and copy the template there
copier copy /path/to/nrp-model-copier /tmp/test-model --trust

# Or use with specific answers
copier copy /path/to/nrp-model-copier /tmp/test-model \
  --data model_name=my_model \
  --data base_model=rdm_complete \
  --trust
```

### Updating Templates

When editing template files:

1. Edit files in `template/` directory (files have `.copier` suffix if configured)
2. Variables use Jinja2 syntax: `{{model_name}}`, `{{model_name|title}}`
3. Base model conditionals use `{% if base_model == "ccmm" %}`
4. Test with `copier copy` to verify output

### Template Inheritance Chains

When modifying templates, understand the inheritance:

**Record Detail** (`record_detail.html`):
```
{{model_name}}/record_detail.html
  → oarepo_ui/record_detail.html
    → invenio_app_rdm/records/detail.html
```

Blocks available: `banners`, `record_body`, `record_sidebar`, `javascript`, `css`, `head_meta`

**Deposit Pages** (`deposit_create.html`, `deposit_edit.html`):
```
{{model_name}}/deposit_*.html
  → oarepo_ui/base_deposit.html
    → invenio_app_rdm/records/deposit.html
```

**Search Page** (`record_search.html`):
```
{{model_name}}/record_search.html
  → oarepo_ui/record_search.html
```

### Key Template Partials

When customizing record detail, edit these partials (not the main template):

- `record_detail/banners.html`: Override banner blocks (`banner_community_header`, `banner_preview_header`, etc.)
- `record_detail/main.html`: Override content blocks (`record_title`, `record_content`, `record_files`)
- `record_detail/javascript.html`: Add page-specific JavaScript

## Common Development Tasks

### Adding a New Base Model Option

1. Add choice to `base_model.choices` in `copier.yml`
2. Add conditional import in `template/{{model_name}}/model.py.copier`
3. Add preset conditional in the presets list within the same file
4. Update `register_to_pyproject.py` if special dependencies are needed

### Adding a New Template Variable

1. Add variable definition to `copier.yml` with type, default, help
2. Use `when: false` to hide from prompts if needed
3. Reference in template files with `{{variable_name}}`
4. Add custom filter to `extensions/` if transformation needed

### Modifying Post-Generation Behavior

Edit `_tasks` in `copier.yml` or the Python scripts in `extensions/`:
- `register_to_pyproject.py`: Modifies pyproject.toml entry points and dependencies
- `register_to_invenio_cfg.py`: Appends registration code to invenio.cfg

### Extending Jinja2 Filters

1. Create new file in `extensions/` following the pattern:
   ```python
   from jinja2.ext import Extension

   def my_filter(value):
       return transformed_value

   class MyExtension(Extension):
       def __init__(self, environment):
           super().__init__(environment)
           environment.filters["my_filter"] = my_filter
   ```
2. Add to `_jinja_extensions` in `copier.yml`

## Related Documentation

- OARepo Documentation: https://github.com/oarepo/oarepo-model
- NRP Documentation: https://nrp-cz.github.io/docs/
- Copier Documentation: https://copier.readthedocs.io/
- Invenio RDM: https://inveniosoftware.org/products/rdm/
