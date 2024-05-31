import time

import duckdb
import streamlit as st
import structlog
from streamlit_dynamic_filters import DynamicFilters

from flusight import DATA_PATH
from flusight.util.logs import setup_logging

setup_logging()
logger = structlog.get_logger()


@st.cache_data
def get_modeL_output_data():
    db_name = str(DATA_PATH / "cdcepi-flusight-forecast-hub.db")

    with duckdb.connect(db_name, read_only=True) as con:
        sql = "SELECT * FROM model_output"
        mo_data = con.sql(sql)
        start = time.process_time()
        # streamlit accepts pandas dataframes, polars dataframes, and arrow tables
        # however, the dynamic filtering widget is designed for pandas (which is slower than polars and arrow)
        mo_data_df = mo_data.to_df()
        logger.info("converted DuckDB query to dataframe", elapsed_time=time.process_time() - start)
        return mo_data_df


def main():
    st.title("CDC FluSight Forecast Hub")
    st.write(
        "This is a test of Streamlit using data from the CDC FluSight Forecast Hub: https://github.com/cdcepi/FluSight-forecast-hub"
    )
    filters = ["model_id", "round_id", "target_end_date", "target", "horizon", "location", "output_type"]
    dynamic_filters = DynamicFilters(df=get_modeL_output_data(), filters=filters)

    # Didn't see a way to set default filter values when instantiating DynamicFilters, so
    # let's set some default values here and update the DynamicFilters object (to prevent too
    # much data being displayed during initial rendering)
    initial_filter = dynamic_filters.filters
    initial_filter["horizon"] = [0]
    initial_filter["location"] = ["US"]
    initial_filter["round_id"] = ["2024-05-04"]
    dynamic_filters.filters = initial_filter

    dynamic_filters.display_filters(location="sidebar")
    dynamic_filters.display_df()

    # line below displays a static version of the dataframe
    # st.write(get_modeL_output_data())


if __name__ == "__main__":
    main()
