#!/usr/bin/env python3
"""
Render an operator specification from YAML metadata and a Jinja template.

Pipeline:

1. Metadata rendering:
   Jinja expressions inside YAML strings are resolved first.
   Example:
       "Avoid undefined behaviour for operator {{ defs.op_name }}"
   becomes:
       "Avoid undefined behaviour for operator **Div**"

2. Metadata enrichment:
   The script expands the common top-level signature into each variant.
   The signature is defined only once in the YAML file:

       signature:
         inputs:
           - name: A
             role: numerator
         outputs:
           - name: C
             role: result

   Type rule:
   - if an argument defines `type` in the common signature, that type is reused
     in every variant;
   - if an argument has no common `type`, the type is generated from the
     variant datatype, for example `real`, `float`, or `int`.

   The script also generates:
   - the mathematical signature expression from the expanded signature;
   - the section title from the operator name and expanded argument types.

   Requirement IDs are NOT generated. They must be entered by the user
   as `req_id` in the YAML file.

3. Validation:
   The script checks that every functional requirement and every constraint has
   a `req_id`, and that all `req_id` values are unique.

4. Document rendering:
   The resolved and enriched metadata is passed to the Markdown Jinja template.

"""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from datetime import datetime, timezone

DEFAULT_REQ_LINK_TEMPLATE = (
    "[<b><span style=\"font-family: 'Courier New', monospace\">"
    "{req_id}</span></b>](#{req_id})"
)

def add_generation_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """
    Add generation metadata to the document.

    The generated date is computed at rendering time.
    """
    result = copy.deepcopy(metadata)

    generation = result.setdefault("generation", {})
    now = datetime.now(timezone.utc)

    generation["date"] = now.strftime("%Y-%m-%d")
    generation["datetime_utc"] = now.strftime("%Y-%m-%d %H:%M:%S UTC")
    generation["iso_datetime_utc"] = now.isoformat()

    return result
    

def make_req_link(req_id: str, metadata: dict[str, Any]) -> str:
    """
    Return a Markdown/HTML hyperlink to a requirement or constraint.

    The hyperlink format can be customized in YAML:

        definitions:
          req_link_template: "...{req_id}..."
    """
    template = (
        metadata.get("definitions", {}).get("req_link_template")
        or DEFAULT_REQ_LINK_TEMPLATE
    )
    return str(template).format(req_id=req_id)


def make_metadata_environment(metadata: dict[str, Any]) -> Environment:
    """
    Build the Jinja environment used to render expressions inside YAML metadata.
    """
    env = Environment(
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=False,
        lstrip_blocks=False,
    )

    # Helper available in YAML strings:
    #   {{ req_link("E_DIV_FLOAT_CONSTR_A_0010") }}
    env.globals["req_link"] = lambda req_id: make_req_link(str(req_id), metadata)

    return env


def render_metadata_value(value: Any, env: Environment, context: dict[str, Any]) -> Any:
    """
    Recursively render every string inside a metadata object.
    """
    if isinstance(value, str):
        return env.from_string(value).render(**context)

    if isinstance(value, list):
        return [render_metadata_value(item, env, context) for item in value]

    if isinstance(value, dict):
        return {
            key: render_metadata_value(item, env, context)
            for key, item in value.items()
        }

    return value


def render_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """
    Render Jinja expressions inside the YAML metadata.

    The context includes the whole metadata tree. Definitions are accessed with:

        {{ defs.my_def }}
    """
    result = copy.deepcopy(metadata)
    env = make_metadata_environment(result)
    return render_metadata_value(result, env, result)


def get_operator_math(metadata: dict[str, Any]) -> str:
    """
    Return the operator representation used in math signatures.

    Preferred source:
        defs.op_math

    Fallback:
        document.operator
    """
    definitions = metadata.get("defs", {})
    if definitions.get("op_math"):
        return str(definitions["op_math"])
    return str(metadata["document"]["operator"])


def get_operator_display(metadata: dict[str, Any]) -> str:
    """
    Return the operator representation used in human-readable titles.

    Preferred source:
        defs.op_name

    Fallback:
        document.operator
    """
    definitions = metadata.get("definitions", {})
    if definitions.get("op_name"):
        return str(definitions["op_name"])
    return str(metadata["document"]["operator"])


def unique_preserve_order(values: list[str]) -> list[str]:
    """
    Return unique values while preserving first occurrence order.
    """
    seen: set[str] = set()
    result: list[str] = []

    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)

    return result


def join_human_list(items: list[str]) -> str:
    """
    Join a list in a readable form.

    [] -> ""
    ["real"] -> "real"
    ["real", "int"] -> "real and int"
    ["real", "float", "int"] -> "real, float, and int"
    """
    if not items:
        return ""

    if len(items) == 1:
        return items[0]

    if len(items) == 2:
        return f"{items[0]} and {items[1]}"

    return ", ".join(items[:-1]) + f", and {items[-1]}"


def get_variant_datatype(variant: dict[str, Any]) -> str:
    """
    Return the datatype associated with a variant section.
    """
    if "datatype" not in variant:
        raise ValueError(
            f"All variants must have a `datatype`. "
        )

    return str(variant["datatype"])


def apply_type_rule(argument: dict[str, Any], variant: dict[str, Any]) -> dict[str, Any]:
    """
    Return a copy of a common-signature argument with the type rule applied.

    If the common signature argument defines `type`, it is reused.
    Otherwise, the type is generated from variant.datatype.
    """
    result = copy.deepcopy(argument)

    if not result.get("type"):
        result["type"] = get_variant_datatype(variant)

    return result


def expand_common_signature(
    common_signature: dict[str, Any],
    variant: dict[str, Any],
) -> dict[str, Any]:
    """
    Create a variant-specific signature from the common top-level signature.
    """
    inputs = common_signature.get("inputs", [])
    outputs = common_signature.get("outputs", [])

    if not inputs:
        raise ValueError("Top-level signature has no inputs")
    if not outputs:
        raise ValueError("Top-level signature has no outputs")

    return {
        "inputs": [apply_type_rule(arg, variant) for arg in inputs],
        "outputs": [apply_type_rule(out, variant) for out in outputs],
    }


def get_signature_types(variant: dict[str, Any]) -> list[str]:
    """
    Return the unique types found in expanded signature inputs and outputs.
    """
    signature = variant.get("signature", {})
    arguments = signature.get("inputs", []) + signature.get("outputs", [])

    types = []
    for item in arguments:
        if "type" not in item:
            raise ValueError(
                f"Signature argument {item.get('name', '<unknown>')} "
                f"in variant {variant.get('id')} has no type"
            )
        types.append(str(item["type"]))

    return unique_preserve_order(types)


def generate_variant_title(metadata: dict[str, Any], variant: dict[str, Any]) -> str:
    """
    Generate a section title from the operator display name and signature types.
    """
    operator_display = get_operator_display(metadata)
    types_text = join_human_list(get_signature_types(variant))

    if not types_text:
        raise ValueError(f"Variant {variant.get('id')} has no signature types")

    return f"Specification of operator {operator_display} for {types_text} values"


def generate_signature_expression(metadata: dict[str, Any], variant: dict[str, Any]) -> str:
    """
    Generate a display-math signature from signature.inputs and signature.outputs.

    Example with one output:
        C = \\textbf{Div}(A, B)

    Example with several outputs:
        A, B = \\textbf{MyOp}(X, Y, Z)
    """
    signature = variant.get("signature", {})

    inputs = signature.get("inputs", [])
    outputs = signature.get("outputs", [])

    if not inputs:
        raise ValueError(f"Variant {variant.get('id')} has no signature.inputs")
    if not outputs:
        raise ValueError(f"Variant {variant.get('id')} has no signature.outputs")

    input_names = ", ".join(str(item["name"]) for item in inputs)
    output_names = ", ".join(str(item["name"]) for item in outputs)
    operator_math = get_operator_math(metadata)

    return f"$$\n{output_names} = {operator_math}({input_names})\n$$"


def enrich_variants(
    metadata: dict[str, Any],
    overwrite_signature: bool = True,
    overwrite_title: bool = True,
) -> dict[str, Any]:
    """
    Add expanded variant.signature, generated signature.expression, and
    generated variant.title to each variant.

    The expanded signature always starts from the top-level common signature.
    """
    result = copy.deepcopy(metadata)

    if "signature" not in result:
        raise ValueError("The YAML file must define a top-level `signature`")

    common_signature = result["signature"]

    for variant in result.get("variants", []):
        if overwrite_signature or "signature" not in variant:
            variant["signature"] = expand_common_signature(common_signature, variant)
        else:
            # Even when keeping a manual signature, ensure missing argument types
            # are completed consistently.
            variant["signature"] = expand_common_signature(variant["signature"], variant)

        variant["signature"]["expression"] = generate_signature_expression(result, variant)

        if overwrite_title or "title" not in variant:
            variant["title"] = generate_variant_title(result, variant)

    return result


def iter_requirement_objects(metadata: dict[str, Any]):
    """
    Yield all objects that must carry a req_id.
    """
    for variant in metadata.get("variants", []):
        variant_id = variant.get("id", "<unknown>")

        for index, req in enumerate(
            variant.get("function", {}).get("requirements", []),
            start=1,
        ):
            yield (
                f"variants[{variant_id}].function.requirements[{index}]",
                req,
            )

        for entity_name, constraints in variant.get("constraints", {}).items():
            for index, constraint in enumerate(constraints, start=1):
                yield (
                    f"variants[{variant_id}].constraints[{entity_name}][{index}]",
                    constraint,
                )


def assert_req_ids_present(metadata: dict[str, Any]) -> None:
    """
    Fail early if any requirement or constraint lacks req_id.
    """
    missing = [
        location
        for location, item in iter_requirement_objects(metadata)
        if not item.get("req_id")
    ]

    if missing:
        raise ValueError(
            "Missing req_id for the following requirement/constraint entries:\n"
            + "\n".join(f"- {location}" for location in missing)
        )


def collect_req_ids(metadata: dict[str, Any]) -> list[str]:
    """
    Collect all user-entered requirement and constraint IDs.
    """
    return [
        str(item["req_id"])
        for _, item in iter_requirement_objects(metadata)
        if item.get("req_id")
    ]


def assert_unique_req_ids(metadata: dict[str, Any]) -> None:
    """
    Fail early if duplicate req_id values exist.
    """
    seen: set[str] = set()
    duplicates: set[str] = set()

    for req_id in collect_req_ids(metadata):
        if req_id in seen:
            duplicates.add(req_id)
        seen.add(req_id)

    if duplicates:
        raise ValueError(
            "Duplicate req_id values found: "
            + ", ".join(sorted(duplicates))
        )


def render_document(
    metadata: dict[str, Any],
    template_path: Path,
    output_path: Path,
) -> None:
    """
    Render the final Markdown document from resolved metadata.
    """
    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Also expose req_link in the final document template, in case the template
    # itself needs to create requirement links.
    env.globals["req_link"] = lambda req_id: make_req_link(str(req_id), metadata)

    template = env.get_template(template_path.name)
    rendered = template.render(**metadata)

    output_path.write_text(rendered, encoding="utf-8")


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise TypeError(f"Expected a YAML mapping at top level in {path}")

    return data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render an operator specification from YAML and Jinja."
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=Path("div.yaml"),
        help="Path to the operator YAML metadata file.",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=Path("operator_spec.md.j2"),
        help="Path to the Markdown Jinja template.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("div.generated.md"),
        help="Path to the generated Markdown output file.",
    )
    parser.add_argument(
        "--resolved-metadata",
        type=Path,
        default=None,
        help="Optional path where the resolved metadata is written.",
    )
    parser.add_argument(
        "--keep-manual-signature",
        action="store_true",
        help=(
            "Keep variant-level manual signatures if they exist. "
            "By default all variant signatures are generated from the top-level signature."
        ),
    )
    parser.add_argument(
        "--keep-manual-title",
        action="store_true",
        help=(
            "Do not overwrite variant.title when it already exists. "
            "By default titles are always regenerated from signature types."
        ),
    )

    args = parser.parse_args()

    metadata = load_yaml(args.metadata)

    # Phase 1: resolve expressions such as {{ defs.op_name }} inside YAML.
    metadata = render_metadata(metadata)

    # Phase 2: enrich metadata.
    metadata = enrich_variants(
        metadata,
        overwrite_signature=not args.keep_manual_signature,
        overwrite_title=not args.keep_manual_title,
    )
    
    metadata = add_generation_metadata(metadata)

    # Phase 3: validate user-provided req_id values.
    assert_req_ids_present(metadata)
    assert_unique_req_ids(metadata)

    # Optional: save the fully resolved YAML.
    if args.resolved_metadata is not None:
        args.resolved_metadata.write_text(
            yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

    # Phase 4: render the final Markdown specification.
    render_document(metadata, args.template, args.output)

    print(f"Generated {args.output}")


if __name__ == "__main__":
    main()
