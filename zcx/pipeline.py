from xarray.coding.pipeline import CoderPipeline
from xarray.namedarray.utils import module_available

conventions = {}


def pipeline() -> CoderPipeline:
    coders = {}

    for name, (coder_cls, deps) in conventions.items():
        if any(not module_available(dep) for dep in deps):
            continue

        coders[name] = coder_cls()

    return CoderPipeline(coders)
