from importlib.resources import files

from cloudpathlib import AnyPath

__version__ = "0.0.1"

# get location of the local duckdb database
LOCAL_DATA_PATH = files("flusight.data").joinpath("cdcepi-flusight-forecast-hub.db")

# set value for the S3 data path
S3_DATA_PATH = AnyPath("s3://bsweger-flusight-forecast/data")
