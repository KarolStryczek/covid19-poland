import dash
import plotly.express as px
from dash.dependencies import Input, Output
import AppUtil
import dash_bootstrap_components as dbc
import NewCasesManager
import layout
import UpdateTwitterData
import threading

stylesheets = dbc.themes.MINTY
app = dash.Dash(__name__, external_stylesheets=[stylesheets])
server = app.server
app.title = "COVID-19 in Poland"
app.layout = layout.prepare_layout

voivodeships, voivodeship_map = AppUtil.get_geojson()

dates = AppUtil.get_dates()
date_from, date_to = min(dates), max(dates)


@app.callback(Output(component_id='cases_map', component_property='figure'),
              Input(component_id='date-picker-range', component_property='start_date'),
              Input(component_id='date-picker-range', component_property='end_date'))
def display_cases_map(start_date, end_date):
    threading.Thread(UpdateTwitterData.update_data()).start()
    global date_from, date_to
    date_from = start_date
    date_to = end_date
    cases = AppUtil.get_cases(date_from, date_to, voivodeship_map)
    fig = px.choropleth(cases, geojson=voivodeships, locations='id', color='cases', hover_name='voivodeship',
                        color_continuous_scale="reds", labels={'cases': 'New cases'})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    return fig


@app.callback(Output(component_id='voivodeship-details', component_property='figure'),
              Output(component_id='details-label', component_property='children'),
              Input(component_id='cases_map', component_property='hoverData'))
def display_details(hover_data):
    if hover_data is not None:
        voivodeship_name = hover_data['points'][0]['hovertext']
        cases = NewCasesManager.get_cases(voivodeship_name, date_from, date_to)
        cases.sort_values(by='date', inplace=True)
        if len(cases) > 1:
            fig = px.line(cases['cases'])
            fig.update_layout(xaxis_title="Data", yaxis_title="Liczba nowych przypadków")
            return fig, f'Województwo: {voivodeship_name}'
        else:
            return px.line(), 'Aby uzyskać wykres zmian w czasie przedział musi być większy niż jeden dzień'

    return px.line(), 'Nakieruj kursor na dowolne województwo aby zobaczyć szczegóły'


if __name__ == '__main__':
    app.run_server(debug=True)
