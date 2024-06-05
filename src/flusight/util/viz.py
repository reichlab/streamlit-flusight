import pandas as pd
import plotly
import plotly.express as px


def create_target_scatterplot(target_data: pd.DataFrame, target: str) -> plotly.graph_objs._figure.Figure:
    """Return the initial scatterplot."""

    location = target_data.iloc[0].location_name
    target_date = target_data.iloc[0].date
    fig = px.scatter(
        target_data,
        title=f"Forecasts of {target} as of {target_date}: {location}",
        x="date",
        y="value",
        labels={"date": "target date", "value": f"{target}"},
        hover_data=["value"],
    )
    fig.update_traces(mode="lines")

    return fig


def add_ribbon(
    fig: plotly.graph_objs._figure.Figure, df: pd.DataFrame, output_type_id: str
) -> plotly.graph_objs._figure.Figure:
    """Add the ribbon to the scatterplot."""

    fig = 1
    return fig
