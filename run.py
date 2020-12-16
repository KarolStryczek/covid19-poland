import dash
import plotly.express as px
from dash.dependencies import Input, Output
from visualization_app import layout
import dash_bootstrap_components as dbc
from acquisition_app import UpdateTwitterData
import threading
from visualization_app import callbacks
from data_access import dao

stylesheets = dbc.themes.MINTY
app = dash.Dash(__name__, external_stylesheets=[stylesheets])
server = app.server
app.title = "COVID-19 w Polsce"
app.layout = layout.prepare_layout
app.config.suppress_callback_exceptions = True


@app.callback(Output(component_id='cases-map', component_property='figure'),
              Input(component_id='date-picker-range', component_property='start_date'),
              Input(component_id='date-picker-range', component_property='end_date'))
def display_cases_map(start_date, end_date):
    return callbacks.prepare_choropleth_map(start_date, end_date)


@app.callback(Output(component_id='voivodeship-details', component_property='figure'),
              Output(component_id='details-label', component_property='children'),
              Input(component_id='cases-map', component_property='hoverData'),
              Input(component_id='date-picker-range', component_property='start_date'),
              Input(component_id='date-picker-range', component_property='end_date'))
def display_details(hover_data, start_date, end_date):
    if hover_data is not None:
        voivodeship_name = hover_data['points'][0]['hovertext']
        cases = dao.get_cases_filtered(voivodeship_name, start_date, end_date)
        cases.sort_values(by='date', inplace=True)
        fig = px.line(cases[['cases', 'date']], x='date', y='cases')
        fig.update_layout(xaxis_title="Data", yaxis_title="Liczba nowych przypadków")
        return fig, f'Województwo: {voivodeship_name}'

    return px.line(), 'Nakieruj kursor na dowolne województwo aby zobaczyć szczegóły'


@app.callback(Output('page-content', 'children'),
              Input('page-tabs', 'value'))
def render_content(tab):
    threading.Thread(target=UpdateTwitterData.update_data).start()
    if tab == 'tab-1':
        return layout.page_1()
    elif tab == 'tab-2':
        return layout.page_2()


if __name__ == '__main__':
    app.run_server(debug=True)
