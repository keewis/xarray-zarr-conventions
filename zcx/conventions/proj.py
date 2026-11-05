from typing import ClassVar

from xarray import Dataset

from zcx.conventions.common import ConventionDefinition, find_convention, has_convention


class ProjCoder:
    kind: ClassVar[str] = "dataset"

    convention_metadata: ClassVar[ConventionDefinition] = {
        "schema_url": "https://raw.githubusercontent.com/zarr-conventions/proj/refs/tags/v0.1/schema.json",
        "spec_url": "https://github.com/zarr-conventions/proj/blob/v0.1/README.md",
        "uuid": "f17cb550-5864-4468-aeb7-f3180cfb622f",
    }

    def encode(self, ds: Dataset) -> Dataset:
        # steps:
        # 0. import xproj
        # 1. find all proj indexes
        # 2. if there's a single index, serialize to group attrs
        # 3. if there's multiple indexes, raise NotImplementedError
        import xproj  # noqa: F401

        crs_aware_indexes = ds.proj.crs_indexes

        if len(crs_aware_indexes) == 0:
            return ds
        elif len(crs_aware_indexes) > 1:
            raise ValueError("only a single crs per dataset is allowed")

    def decode(self, ds: Dataset) -> Dataset:
        # steps:
        # 0. import xproj
        # 1. assemble a list of datasets (group-level and variables converted to single-variable datasets) that have the proj convention defined
        # 2. raise NotImplementedError for array proj metadata
        # 3. call ds.proj.assign_crs the dataset with the proj metadata
        import xproj  # noqa: F401

        variable_conventions = {
            name: var
            for name, var in ds.variables.items()
            if has_convention(var.attrs, self.convention_metadata)
        }

        if variable_conventions:
            raise ValueError(
                "per-variable conventions are not supported, yet."
                f" Found in: {', '.join(sorted(variable_conventions))}."
            )

        index = find_convention(ds.attrs, self.convention_metadata)
        if index == -1:
            return ds

        if (proj := ds.attrs.get("proj:code")) is not None:
            pass
        elif (proj := ds.attrs.get("proj:wkt2")) is not None:
            pass
        elif (proj := ds.attrs.get("proj:projjson")) is not None:
            pass
        else:
            raise ValueError("proj convention declared but no settings found.")

        return ds.proj.assign_crs({"crs": proj})
