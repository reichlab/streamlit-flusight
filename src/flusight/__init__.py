from importlib import resources

from cloudpathlib import AnyPath

__version__ = "0.0.1"

MODULE_PATH = AnyPath(resources.files("flusight")).parent
LOCAL_DATA_PATH = MODULE_PATH / "data"
S3_DATA_PATH = AnyPath("s3://bsweger-flusight-forecast/data")
