import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go


def create_target_scatterplot(target_data: pd.DataFrame, target: str) -> plotly.graph_objs._figure.Figure:
    """Return the initial scatterplot."""

    location = target_data.iloc[0].location_name
    fig = px.scatter(
        target_data,
        title=f"Forecasts of {target} for round_id 2024-05-04: {location}",
        x="date",
        y="value",
        labels={"date": "target date", "value": f"{target}"},
        hover_data=["value"],
    )
    fig.update_traces(mode="lines", name="target_data")
    fig.update_layout(title_x=0.1, title_font_color="grey", title={"font": {"size": 25}})

    return fig


# TODO: determine the correct function signature/stop hard-coding
def plot_model_forecast(
    fig_target: plotly.graph_objs._figure.Figure, model_data: list[pd.DataFrame], output_type_id: str
) -> plotly.graph_objs._figure.Figure:
    """Add model forecast data to the target plot."""

    # hard code this for now
    output_type_id = "0.5"
    output_type_id_upper = "0.95"
    output_type_id_lower = "0.1"

    hover_text = "value: %{y}<br>date: %{x}"

    for mo in model_data:
        # workaround until we stop allowing users to select models
        # that don't have submissions for the currently selected round_id
        try:
            model_id = mo["model_id"].iloc[0]
        except IndexError:
            continue

        # grab the values we want on the line (the demo is limited to quantile output types, so
        # we'll just make them numeric for df manipulation)
        prediction_values = mo[mo["output_type_id"] == float(output_type_id)]
        prediction_values_upper = mo[mo["output_type_id"] == float(output_type_id_upper)]["value"].tolist()
        prediction_values_lower = mo[mo["output_type_id"] == float(output_type_id_lower)]["value"].tolist()

        fig_target.add_trace(
            go.Scatter(
                x=prediction_values["target_end_date"],
                y=prediction_values["value"],
                mode="lines",
                name=model_id,
                legendgroup=model_id,
                hoverinfo="y",
                hovertemplate=hover_text,
            )
        )

        # add the upper and lower bounds as a single trace, using
        # the technique described here:
        # https://plotly.com/python/continuous-error-bars/
        fig_target.add_trace(
            go.Scatter(
                x=prediction_values["target_end_date"].tolist() + prediction_values["target_end_date"].tolist()[::-1],
                y=prediction_values_upper + prediction_values_lower[::-1],
                name=model_id,
                mode="lines",
                line=dict(width=0),
                fill="toself",
                hoverinfo="skip",
                legendgroup=model_id,
                showlegend=False,
            )
        )

    return fig_target
