"""Entry-point shim for the pptify CLI, referenced by [project.scripts] in pyproject.toml.

This module loads pptify-cli/__main__.py via importlib so the dash-named
directory does not need to be a valid Python package name.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def main() -> None:
    _main_path = Path(__file__).parent / "pptify-cli" / "__main__.py"
    spec = importlib.util.spec_from_file_location("_pptify_cli_main", _main_path)
    if spec is None or spec.loader is None:  # pragma: no cover
        raise RuntimeError(f"Cannot load pptify-cli entry point from: {_main_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_pptify_cli_main"] = mod
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    mod.main(sys.argv[1:])


if __name__ == "__main__":
    main()
