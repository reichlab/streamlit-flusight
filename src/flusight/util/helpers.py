import duckdb
import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/amp/
    HONESTLY STREAMLIT SHOULD HAVE THIS OUT OF THE BOX AND SUPPORT THINGS BESIDES PANDAS, C'MON 😠
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter model outputs on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


def filter_duckdb(query: duckdb.duckdb.DuckDBPyRelation) -> duckdb.duckdb.DuckDBPyRelation:
    """
    Modify the Steamlit filter UI to work with duckdb query objects instead of dataframes,
    so we can output the result to a polars dataframe for better performance.
    (this is WIP--not even sure it's a good idea)
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return query.pl()

    # don't really need to do this every time, but for expediency...
    # if we want to be really fancy, we *could* look at the information_schema, or example:
    # SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'model_output';
    # columns = query.columns
    # data_types = query.types
    # schema = {col: type for col, type in zip(columns, data_types)}

    # Try to convert datetimes into a standard format (datetime, no timezone)
    # (this is the old pandas-based code)
    # for col in query.columns:
    #     if is_object_dtype(df[col]):
    #         try:
    #             df[col] = pd.to_datetime(df[col])
    #         except Exception:
    #             pass

    #     if is_datetime64_any_dtype(df[col]):
    #         df[col] = df[col].dt.tz_localize(None)

    # modification_container = st.container()

    # with modification_container:
    #     to_filter_columns = st.multiselect("Filter model outputs on", query.columns)
    #     for column in to_filter_columns:
    #         left, right = st.columns((1, 20))
    #         # Treat columns with < 10 unique values as categorical
    #         if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
    #             user_cat_input = right.multiselect(
    #                 f"Values for {column}",
    #                 df[column].unique(),
    #                 default=list(df[column].unique()),
    #             )
    #             df = df[df[column].isin(user_cat_input)]
    #         elif is_numeric_dtype(df[column]):
    #             _min = float(df[column].min())
    #             _max = float(df[column].max())
    #             step = (_max - _min) / 100
    #             user_num_input = right.slider(
    #                 f"Values for {column}",
    #                 min_value=_min,
    #                 max_value=_max,
    #                 value=(_min, _max),
    #                 step=step,
    #             )
    #             df = df[df[column].between(*user_num_input)]
    #         elif is_datetime64_any_dtype(df[column]):
    #             user_date_input = right.date_input(
    #                 f"Values for {column}",
    #                 value=(
    #                     df[column].min(),
    #                     df[column].max(),
    #                 ),
    #             )
    #             if len(user_date_input) == 2:
    #                 user_date_input = tuple(map(pd.to_datetime, user_date_input))
    #                 start_date, end_date = user_date_input
    #                 df = df.loc[df[column].between(start_date, end_date)]
    #         else:
    #             user_text_input = right.text_input(
    #                 f"Substring or regex in {column}",
    #             )
    #             if user_text_input:
    #                 df = df[df[column].astype(str).str.contains(user_text_input)]

    # return df
