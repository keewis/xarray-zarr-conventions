from typing import Any, TypedDict


def _matches_schema_url(actual: str, definition: str) -> bool:
    # TODO: support versions
    return actual == definition


def _matches_spec_url(actual: str, definition: str) -> bool:
    # TODO: support versions
    return actual == definition


convention_declaration: str = "zarr_conventions"


class ConventionDefinition(TypedDict):
    uuid: str
    schema_url: str
    spec_url: str


def compare_convention(
    convention: dict[str, str], definition: ConventionDefinition
) -> bool:
    return (
        convention.get("uuid") == definition["uuid"]
        or _matches_schema_url(convention.get("schema_url"), definition["schema_url"])
        or _matches_spec_url(convention.get("spec_url"), definition["spec_url"])
    )


def has_convention(attrs: dict[str, Any], definition: ConventionDefinition) -> bool:
    conventions = attrs.get(convention_declaration)
    if conventions is None or not conventions:
        return False

    return any(compare_convention(convention, definition) for convention in conventions)


def find_convention(attrs: dict[str, Any], definition: ConventionDefinition) -> int:
    conventions = attrs.get(convention_declaration)
    if conventions is None or not conventions:
        conventions = []

    for index, convention in enumerate(conventions):
        if compare_convention(convention, definition):
            return index

    return -1
