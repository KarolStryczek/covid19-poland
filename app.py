import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import NewCasesManager
import AppUtil
import dash_bootstrap_components as dbc

stylesheets = dbc.themes.MINTY
app = dash.Dash(__name__, external_stylesheets=[stylesheets])
server = app.server

dates = AppUtil.get_dates()
date_min, date_max = min(dates), max(dates)

app.layout = html.Div(
    children=[
        html.H1(children='COVID-19 New cases'),

        html.Div(children='Map below shows new COVID-19 cases in given period'),

        dcc.Graph(
            id='choropleth',
            style={
                'height': 500,
                'width': 900,
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
            },
        ),

        html.Div(
            children=dcc.DatePickerRange(
                id='date-picker-range',
                display_format='MM-D-Y',
                min_date_allowed=date_min,
                max_date_allowed=date_max,
                initial_visible_month=date_max,
                start_date=date_min,
                end_date=date_max
            ),
        )
    ],
    style={
        'margin-top': '30px',
        'textAlign': 'center',
    }
)


@app.callback(Output(component_id='choropleth', component_property='figure'),
              [Input(component_id='date-picker-range', component_property='start_date'),
               Input(component_id='date-picker-range', component_property='end_date')])
def display_choropleth(date_from, date_to):
    voivodeships, voivodeship_map = AppUtil.get_geojson()
    cases = NewCasesManager.get_cases_grouped(date_from=date_from, date_to=date_to)
    cases = NewCasesManager.populate_cases_with_ids(cases, voivodeship_map)
    fig = px.choropleth(cases, geojson=voivodeships, locations='id', color='cases', hover_name='voivodeship',
                        color_continuous_scale="reds", labels={'cases': 'New cases'})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
