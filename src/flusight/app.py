from importlib.resources import files

import streamlit as st
import structlog
from st_aggrid import AgGrid  # noqa
from streamlit_dynamic_filters import DynamicFilters  # noqa

# from flusight import LOCAL_DATA_PATH as local_data_path
from flusight.util.data import get_locations, get_model_output_location_outcome, get_outcomes
from flusight.util.logs import setup_logging

setup_logging()
logger = structlog.get_logger()


def main():
    """Main function for running the Streamlit app."""
    local_data_path = files("flusight.data").joinpath("cdcepi-flusight-forecast-hub.db")
    db_location = str(local_data_path)

    st.title("Streamlit Spike")
    st.write(
        """
        This is a test page to see how Streamlit fares when trying to recreate the following
        COVID-19 Forecast Hub visualization:
        https://viz.covid19forecasthub.org/
        """
    )
    st.write(
        "This is a single page Streamlit app, created with data from the CDC FluSight Forecast Hub: https://github.com/cdcepi/FluSight-forecast-hub"
    )

    # temporary, so we can view the format of the target_data and models selections
    target_data = "2024-05-25"
    models = "FluSight-ensemble"

    st.write(f"Target Data: {target_data}")
    st.write(f"Models: {models}")

    with st.sidebar:
        location = st.selectbox(
            "Location",
            get_locations(db_location),
            index=59,  # this is cheating
        )

        outcome = st.selectbox(
            "Outcome",
            get_outcomes(db_location),
            index=0,  # more cheating
        )

        target_data = st.multiselect(
            "Select Target Data:",
            get_model_output_location_outcome(db_location, location, outcome)["target_end_date"].unique(),
            max_selections=2,
            placeholder="2024-05-25",
        )

        models = st.multiselect(
            "Select Models:",
            get_model_output_location_outcome(db_location, location, outcome)["model_id"].unique(),
            placeholder="FluSight-ensemble",
        )

    st.dataframe(get_model_output_location_outcome(db_location, location, outcome))


if __name__ == "__main__":
    main()
