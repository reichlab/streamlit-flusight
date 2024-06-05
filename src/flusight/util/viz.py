import plotly.express as px


def create_scatterplot(df, target, location, round):
    """Return the initial scatterplot."""

    fig = px.scatter(
        df,
        title=f"Forecasts of {target} in {location} as of round {round}",
        x="target_end_date",
        y="value",
        color="model_id",
        symbol="model_id",
        labels={"model_id": "model", "target_end_date": "target end date", "value": f"{target}"},
        hover_data=["value"],
    )
    fig.update_traces(mode="lines+markers")

    return fig
