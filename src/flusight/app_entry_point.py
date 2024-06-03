"""File to run the Streamlit app."""

import runpy
import sys
from importlib.resources import files

import structlog

import flusight

logger = structlog.get_logger()


def main() -> None:
    """Start and run the Streamlit app."""

    # get path of the streamlit app
    streamlit_app_path = str(files(flusight).joinpath("app.py"))
    logger.info("Running Streamlit app", path=streamlit_app_path)
    sys.argv = ["streamlit", "run", streamlit_app_path]
    runpy.run_module("streamlit", run_name="__main__")


if __name__ == "__main__":
    main()
