import duckdb
import pandas as pd
import streamlit as st


@st.cache_data
def get_model_output_location_outcome(db_location: str, location: str, outcome: str) -> pd.DataFrame:
    with duckdb.connect(db_location, read_only=True) as con:
        con.sql("INSTALL httpfs;")
        con.sql("SET http_keep_alive=false;")
        sql = f"""
        SELECT *
        FROM model_output
        WHERE
            output_type = 'quantile'
            AND location = '{location}'
            AND target = '{outcome}'
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
def get_outcomes(db_location: str) -> pd.Series:
    with duckdb.connect(db_location, read_only=True) as con:
        con.sql("INSTALL httpfs;")
        con.sql("SET http_keep_alive=false;")
        sql = """
        SELECT DISTINCT target as outcome
        FROM model_output
        WHERE output_type = 'quantile'
        ORDER BY target
        """
        outcomes = con.sql(sql)
        return outcomes.to_df()["outcome"]
