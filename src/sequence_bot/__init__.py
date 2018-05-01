from . import sequencer

from ._version import get_versions
__version__: str = get_versions()['version']  # type: ignore
del get_versions
