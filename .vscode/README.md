# VS Code Settings for Pylance

This directory contains recommended VS Code settings for the project.

## Setup

Copy `settings.json.example` to `settings.json`:

```bash
# On Windows (PowerShell)
Copy-Item .vscode\settings.json.example .vscode\settings.json

# On Linux/Mac
cp .vscode/settings.json.example .vscode/settings.json
```

## What These Settings Do

The `settings.json.example` file configures Pylance (Python language server) to:

1. **Suppress Type Inference Warnings**: Disables hundreds of false-positive warnings about unknown types in pandas, sklearn, and matplotlib
2. **Enable Useful Warnings**: Keeps warnings for unused imports, variables, and functions
3. **Configure Formatting**: Sets Ruff as the default Python formatter
4. **Optimize Performance**: Excludes cache directories and sets appropriate indexing depth for large packages

## Already Using pyrightconfig.json

This project also includes `pyrightconfig.json` in the root directory, which provides project-level type checking configuration that works across all editors (VS Code, PyCharm, etc.).

The `.vscode/settings.json` file provides additional VS Code-specific UI and editor behavior settings.
