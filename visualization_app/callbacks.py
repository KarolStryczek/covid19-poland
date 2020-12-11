from visualization_app import AppUtil
import plotly.express as px


def prepare_choropleth_map_from_cases(cases, voivodeships):
    fig = px.choropleth(
        data_frame=cases,
        geojson=voivodeships,
        locations='id',
        color='cases',
        hover_name='voivodeship',
        color_continuous_scale="reds",
        labels={'cases': "Nowe przypadki"},
        hover_data={'id': False}
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


def prepare_choropleth_map(start_date, end_date):
    cases, voivodeships = AppUtil.get_cases_and_voivodeships(start_date, end_date)
    return prepare_choropleth_map_from_cases(cases, voivodeships)

