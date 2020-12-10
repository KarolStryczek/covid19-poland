from visualization_app import AppUtil
import plotly.express as px


def prepare_choropleth_map(start_date, end_date):
    voivodeships, voivodeship_map = AppUtil.get_geojson()
    cases = AppUtil.get_cases(start_date, end_date, voivodeship_map)
    fig = px.choropleth(cases, geojson=voivodeships, locations='id', color='cases', hover_name='voivodeship',
                        color_continuous_scale="reds", labels={'cases': "Nowe przypadki"}, hover_data={'id': False})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        dragmode=False
    )
    return fig


def prepare_choropleth_map_new_cases():
    new_date = max(AppUtil.get_dates())
    return prepare_choropleth_map(new_date, new_date), new_date
