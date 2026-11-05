from typing import ClassVar, Literal, Self

from xarray import Dataset


class SpatialCoder:
    kind: ClassVar[Literal["dataset"]] = "dataset"

    def configure(self, **settings) -> Self:
        if settings:
            raise TypeError(f"unknown settings: {list(settings)}")
        return self

    def decode(self, ds: Dataset) -> Dataset:
        pass

    def encode(self, ds: Dataset) -> Dataset:
        pass
