from visualization_app import AppUtil
import plotly.express as px
import plotly
import pandas as pd
from typing import Dict


def prepare_choropleth_map_from_cases(cases: pd.DataFrame, voivodeships: Dict) -> plotly.graph_objs.Figure:
    fig = px.choropleth(
        data_frame=cases,
        geojson=voivodeships,
        locations='id',
        color='cases',
        hover_name='voivodeship',
        color_continuous_scale="reds",
        labels={'cases': "Nowe przypadki"},
        # hover_data={'id': False}
    )
    fig.update_geos(
        fitbounds="locations",
        visible=False
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        dragmode=False
    )
    return fig


def prepare_choropleth_map(start_date: AppUtil.any_date, end_date: AppUtil.any_date) -> plotly.graph_objs.Figure:
    cases, voivodeships = AppUtil.get_cases_and_voivodeships(start_date, end_date)
    return prepare_choropleth_map_from_cases(cases, voivodeships)


def prepare_details_graph(cases: pd.DataFrame) -> plotly.graph_objs.Figure:
    voivodeship_name = cases.head(1).voivodeship.values[0]
    fig = px.line(cases[['cases', 'date']], x='date', y='cases')
    fig.update_layout(
        title=f'Województwo {voivodeship_name}',
        xaxis_title="Data",
        yaxis_title="Liczba nowych przypadków")
    return fig
