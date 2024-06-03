import time
from importlib.resources import files

import duckdb
import pandas as pd
import streamlit as st
import structlog
from st_aggrid import AgGrid  # noqa
from streamlit_dynamic_filters import DynamicFilters  # noqa

# from flusight import LOCAL_DATA_PATH as local_data_path
from flusight.util.helpers import filter_dataframe
from flusight.util.logs import setup_logging

setup_logging()
logger = structlog.get_logger()


@st.cache_data
def get_model_output_aggregates(db_location: str) -> pd.DataFrame:
    with duckdb.connect(db_location, read_only=True) as con:
        con.sql("INSTALL httpfs;")
        con.sql("SET http_keep_alive=false;")
        sql = """
        SELECT
          model_id as 'Model',
          COUNT(DISTINCT reference_date) as 'Total Submissions',
          MAX(reference_date) as 'Latest Submission'
        FROM model_output
        GROUP BY ALL
        ORDER BY model_id
        """
        mo_agg = con.sql(sql)
        return mo_agg.to_df()


@st.cache_data
def get_modeL_output_data(db_location: str) -> pd.DataFrame:
    with duckdb.connect(db_location, read_only=True) as con:
        # Because the front-end components rely on pandas which is sloooooow, this prototype
        # artificially limits the number of rows being returned via a WHERE clause
        con.sql("INSTALL httpfs;")
        con.sql("SET http_keep_alive=false;")
        sql = """
        SELECT *
        FROM model_output
        WHERE
          DATEPART('year', reference_date) = 2024
          AND date_part('month', reference_date) in (4, 5)
          AND horizon=0
        """
        mo_data = con.sql(sql)
        start = time.process_time()
        # streamlit accepts pandas dataframes, polars dataframes, and arrow tables
        # however, a lot of widgets/code seem designed for pandas (which is slower than polars and arrow)
        mo_data_df = mo_data.to_df()
        logger.info("converted DuckDB query to dataframe", elapsed_time=time.process_time() - start)
        return mo_data_df


def main():
    """Main function for running the Streamlit app."""
    local_data_path = files("flusight.data").joinpath("cdcepi-flusight-forecast-hub.db")
    db_location = str(local_data_path)

    st.title("CDC FluSight Forecast Hub")
    st.write("🚧 🚧 🚧 🚧")
    st.write(
        "This is a single page Streamlit app, created with data from the CDC FluSight Forecast Hub: https://github.com/cdcepi/FluSight-forecast-hub"
    )

    st.title("Submission Information")
    agg_data = get_model_output_aggregates(db_location)
    st.dataframe(agg_data)

    st.html("<hr>")
    st.write("Maybe someone better at charts should do this part...")

    st.bar_chart(data=agg_data, x="Total Submissions", y="Model", use_container_width=True)

    st.title("Detailed Model Output Data")

    df = get_modeL_output_data(db_location)
    AgGrid(filter_dataframe(df))

    ###############################################################################################
    # The code below uses a DynamicFilters widget which is less flexible but is nicer looking
    # than Streamlit's out-of-the-box dataframe widget or the AgGrid widget we're using above.
    ###############################################################################################
    # st.dataframe(filter_dataframe(df))
    # filters = ["model_id", "round_id", "target_end_date", "target", "horizon", "location", "output_type"]
    # dynamic_filters = DynamicFilters(df=get_modeL_output_data(db_location), filters=filters)

    # # Didn't see a way to set default filter values when instantiating DynamicFilters, so
    # # let's set some default values here and update the DynamicFilters object (to prevent too
    # # much data being displayed during initial rendering)
    # initial_filter = dynamic_filters.filters
    # initial_filter["horizon"] = [0]
    # initial_filter["location"] = ["US"]
    # initial_filter["round_id"] = ["2024-05-04"]
    # dynamic_filters.filters = initial_filter

    # dynamic_filters.display_filters(location="sidebar")
    # dynamic_filters.display_df()

    # line below displays a static version of the dataframe
    # st.write(get_modeL_output_data())


if __name__ == "__main__":
    main()
