import duckdb
import pandas as pd
import streamlit as st

from flusight import LOCAL_TARGET_DATA_PATH as target_data_path


@st.cache_data
def get_target_data(db_location: str, target: str, target_date: str = None, location: str = None) -> pd.DataFrame:
    """Retrieve the hub's target data."""

    # TODO: add target data as a table in the DuckDB file. For now, just
    # grab the .csv from disk
    target_data = pd.read_csv(str(target_data_path))
    if target_date:
        target_data = target_data[target_data.date == target_date]
    if location:
        target_data = target_data[target_data.location == location]

    return target_data


@st.cache_data
def get_model_output_location_target(db_location: str, location: str, target: str) -> pd.DataFrame:
    with duckdb.connect(db_location, read_only=True) as con:
        con.sql("INSTALL httpfs;")
        con.sql("SET http_keep_alive=false;")
        sql = f"""
        SELECT * EXCLUDE (output_type_id)
          , CAST(output_type_id AS DECIMAL(3,2)) AS output_type_id
        FROM model_output
        WHERE
            output_type = 'quantile'
            AND location = '{location}'
            AND target = '{target}'
        """
        mo = con.sql(sql)
        return mo.to_df()


@st.cache_data
def get_locations(db_location: str) -> pd.Series:
    with duckdb.connect(db_location, read_only=True) as con:
        con.sql("INSTALL httpfs;")
        con.sql("SET http_keep_alive=false;")
        sql = """
        SELECT DISTINCT location
        FROM model_output
        WHERE output_type = 'quantile'
        ORDER BY location
        """
        locations = con.sql(sql)
        return locations.to_df()["location"]


@st.cache_data
def get_targets(db_location: str) -> pd.Series:
    with duckdb.connect(db_location, read_only=True) as con:
        con.sql("INSTALL httpfs;")
        con.sql("SET http_keep_alive=false;")
        sql = """
        SELECT DISTINCT target
        FROM model_output
        WHERE output_type = 'quantile'
        ORDER BY target
        """
        targets = con.sql(sql)
        return targets.to_df()


@st.cache_data
def get_output_type_ids(db_location: str) -> pd.Series:
    with duckdb.connect(db_location, read_only=True) as con:
        con.sql("INSTALL httpfs;")
        con.sql("SET http_keep_alive=false;")
        sql = """
        SELECT DISTINCT output_type_id
        FROM model_output
        WHERE output_type = 'quantile'
        ORDER BY output_type_id
        """
        output_type_ids = con.sql(sql)
        return output_type_ids.to_df()


# @st.cache_data
# def get_model_ids(db_location: str) -> pd.Series:
#     with duckdb.connect(db_location, read_only=True) as con:
#         con.sql("INSTALL httpfs;")
#         con.sql("SET http_keep_alive=false;")
#         sql = """
#         SELECT DISTINCT model_id
#         FROM model_output
#         WHERE output_type = 'quantile'
#         ORDER BY model_id
#         """
#         model_ids = con.sql(sql)
#         return model_ids.to_df()
