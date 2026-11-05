from typing import ClassVar, Literal, Self

from xarray import Dataset

from zcx.conventions.common import ConventionDefinition, has_convention


class DggsCoder:
    kind: ClassVar[Literal["dataset"]] = "dataset"

    convention_definition: ClassVar[ConventionDefinition] = {
        "uuid": "7b255807-140c-42ca-97f6-7a1cfecdbc38",
        "schema_url": "https://raw.githubusercontent.com/zarr-conventions/dggs/refs/tags/v1/schema.json",
        "spec_url": "https://github.com/zarr-conventions/dggs/blob/v1/README.md",
    }

    def configure(self, **settings) -> Self:
        if settings:
            raise TypeError("dggs: coder does not have settings")
        return self

    def decode(self, ds: Dataset) -> Dataset:
        import xdggs  # noqa: F401

        if any(
            has_convention(var.attrs, self.convention_definition)
            for var in ds.variables.values()
        ):
            raise NotImplementedError(
                "dggs: multiple definitions on the same dataset are not supported yet"
            )

        if not has_convention(ds.attrs, self.convention_definition):
            return ds

        return ds.dggs.decode(convention="zarr")

    def encode(self, ds: Dataset) -> Dataset:
        import xdggs  # noqa: F401

        try:
            ds.dggs.index
        except ValueError as e:
            raise ValueError("dggs: no dggs index found") from e

        return ds.dggs.encode(convention="zarr")
