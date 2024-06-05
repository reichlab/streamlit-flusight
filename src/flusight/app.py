from importlib.resources import files

import plotly.express as px
import streamlit as st
import structlog
from st_aggrid import AgGrid  # noqa
from streamlit_dynamic_filters import DynamicFilters  # noqa

# from flusight import LOCAL_DATA_PATH as local_data_path
from flusight.util.data import get_locations, get_model_output_location_target, get_targets
from flusight.util.logs import setup_logging

setup_logging()
logger = structlog.get_logger()


# TODOs:
# 1. filters aren't working quite right...the way we're creating a variable to hold
# the filtered dataframe isn't triggering whatever mechanism tells Streamlit to
# update its components
# 2. color the scatterplot dots/lines based on model_id
# 3. plot the target data
# 4. add the distribution (quantiles) + corresponding drop-down
# ?? would we ever plot more than one output type on this graph?


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

    with st.sidebar:
        location = st.selectbox(
            "Location",
            get_locations(db_location),
            index=59,  # this is cheating
        )

        target = st.selectbox(
            "Target",
            get_targets(db_location),
            index=0,  # more cheating
        )

        # TODO: disable/remove target data options that don't meet other filtering criteria
        round_id_values = (
            get_model_output_location_target(db_location, location, target)["round_id"]
            .drop_duplicates()
            .sort_values(ascending=False)
        )
        round = st.selectbox(
            "Select Round Id:",
            round_id_values,
            index=0,
        )

        # TODO: disable/remove models that don't meet other filtering criteria
        models_values = (
            get_model_output_location_target(db_location, location, target)["model_id"].drop_duplicates().sort_values()
        )
        models = st.multiselect(
            "Select Models:",
            models_values,
            default=models_values[models_values == "FluSight-ensemble"],
        )

    render = get_model_output_location_target(db_location, location, target)
    if round:
        render = render[render["round_id"] == round]
    if models:
        render = render[render["model_id"].isin(models)]

    fig = px.scatter(
        render,
        title=f"Forecasts of {target} in {location} as of round {round}",
        x="target_end_date",
        y="value",
        color="model_id",
        symbol="model_id",
        labels={"model_id": "model", "target_end_date": "target end date", "value": f"{target}"},
        hover_data=["value"],
    )
    fig.update_traces(mode="lines+markers")
    st.plotly_chart(fig, key="scatter", on_select="rerun")

    # this is here for reference, to make sure the filters are working as intended
    st.dataframe(render)


if __name__ == "__main__":
    main()


# interesting test cases
# model_id = "UGA_flucast-OKeeffe"
# this model only has 3 submissions
# round_ids = 2023-10-14, 2023-10-21, 2023-10-28
