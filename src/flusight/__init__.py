from importlib import resources

from cloudpathlib import AnyPath

__version__ = "0.0.1"

MODULE_PATH = AnyPath(resources.files("flusight")).parent
DATA_PATH = MODULE_PATH / "data"
