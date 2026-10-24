"""Command-line entry point for converting a simulation config into a BOM."""

import argparse
import json
from pathlib import Path
from typing import Any


def config_to_bom(config: dict[str, Any]) -> dict[str, Any]:
    """Build a normalized bill of materials from a project configuration."""
    components = config.get("components", [])
    bom: list[dict[str, Any]] = []

    for component in components:
        if not isinstance(component, dict):
            raise ValueError("Each component must be an object")

        name = component.get("name")
        quantity = component.get("quantity", 1)
        if not name or not isinstance(quantity, (int, float)) or quantity < 0:
            raise ValueError(
                "Each component needs a name and a non-negative numeric quantity"
            )

        bom.append(
            {
                "name": name,
                "quantity": quantity,
                "unit": component.get("unit", "each"),
            }
        )

    return {
        "project": config.get("project", "simulation"),
        "items": bom,
        "total_line_items": len(bom),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a simulation configuration into a bill of materials."
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Path to a JSON configuration file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write the BOM to this JSON file instead of stdout",
    )
    args = parser.parse_args()

    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError("The configuration root must be a JSON object")
        bom = config_to_bom(config)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))

    output = json.dumps(bom, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
