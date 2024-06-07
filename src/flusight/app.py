from importlib.resources import files

import streamlit as st
import structlog

# from flusight import LOCAL_DATA_PATH as local_data_path
from flusight.util.data import (
    get_locations,
    get_model_output_location_target,
    get_output_type_ids,
    get_target_data,
    get_targets,
)
from flusight.util.helpers import get_round
from flusight.util.logs import setup_logging
from flusight.util.viz import create_target_scatterplot, plot_model_forecast

setup_logging()
logger = structlog.get_logger()


# TODOs:
# 2. color the scatterplot dots/lines based on model_id
# 4. add the distribution (quantiles) + corresponding drop-down
# 7. Update select box options based on other selections (e.g., don't display models w/o submissions for the selected round_id)
# ?? would we ever plot more than one output type on this graph?


def main():
    """Main function for running the Streamlit app."""
    local_data_path = files("flusight.data").joinpath("cdcepi-flusight-forecast-hub.db")
    db_location = str(local_data_path)

    st.set_page_config(layout="wide")
    if "round_id" not in st.session_state:
        st.session_state["round_id"] = "2024-05-04"

    st.title("Streamlit Spike")
    st.write(
        """
        This is a test page to see how Streamlit fares when trying to recreate the following
        COVID-19 Forecast Hub visualization:
        https://viz.covid19forecasthub.org/
        """
    )
    st.write(
        "The chart is generated with quantile-type forecasts from the CDC FluSight Forecast Hub: https://github.com/cdcepi/FluSight-forecast-hub"
    )

    with st.sidebar:
        # TODO: pull location list from the target data so we can use state names instead of FIPS code
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

        output_type_id = st.selectbox(
            "Output Type ID",
            get_output_type_ids(db_location),
            index=0,
        )

        target_date = st.selectbox(  # noqa
            "Target Date:",
            get_target_data(db_location, target)["date"].drop_duplicates().sort_values(ascending=False),
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

    mo = get_model_output_location_target(db_location, location, target)
    if models:
        mo = mo[mo["model_id"].isin(models)]
    if st.session_state.round_id:
        mo = mo[mo["round_id"] == st.session_state.round_id]

    target_data = get_target_data(db_location, target, location=location)
    model_predictions = [mo[mo.model_id == model] for model in models]

    fig = create_target_scatterplot(target_data, target, st.session_state.round_id)
    fig = plot_model_forecast(fig, model_predictions, output_type_id)

    # uncomment below to see the figure's underlying data for debugging
    # fig_data = fig.data
    # fig_data

    st.header("Forecast Viz")
    st.plotly_chart(fig, key="scatter", on_select="rerun", use_container_width=True)

    previous, next = st.columns(2, gap="small")
    with previous:
        st.button(
            "Previous Round",
            help="display the last forecast submission round",
            on_click=lambda: st.session_state.update(round_id=get_round(st.session_state.round_id, "previous")),
        )
    with next:
        st.button(
            "Next Round",
            help="display the next forecast submission round",
            on_click=lambda: st.session_state.update(round_id=get_round(st.session_state.round_id, "next")),
        )

    st.html("<hr>")
    st.header("Supporting Data")
    # this is here for reference, to make sure the filters are working as intended
    st.dataframe(mo)


if __name__ == "__main__":
    main()


# interesting test cases
# model_id = "UGA_flucast-OKeeffe"
# this model only has 3 submissions
# round_ids = 2023-10-14, 2023-10-21, 2023-10-28
