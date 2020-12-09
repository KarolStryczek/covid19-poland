import dash_core_components as dcc
import dash_html_components as html
import AppUtil
import datetime as dt


def prepare_layout():
    dates = AppUtil.get_dates()
    date_min, date_max = min(dates), max(dates)
    date_max_next_day = dt.datetime.strptime(date_max, '%Y-%m-%d') + dt.timedelta(days=1)

    layout = html.Div(
        [
            html.H1(children='Zachorowania na COVID-19'),

            html.Div(children='Poniższa mapa pokazuje nowe zachorowania w zadanym okresie'),

            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(
                                id='cases_map',
                                style={
                                    'height': '100%',
                                    'width': '100%',
                                    "display": "block",
                                    "margin-left": "auto",
                                    "margin-right": "auto",
                                },
                            ),

                            html.Div(
                                children=dcc.DatePickerRange(
                                    id='date-picker-range',
                                    display_format='DD-MM-YYYY',
                                    minimum_nights=0,
                                    with_portal=True,
                                    min_date_allowed=date_min,
                                    max_date_allowed=date_max_next_day,
                                    initial_visible_month=date_max,
                                    start_date=date_max,
                                    end_date=date_max
                                ),
                            ),
                        ],
                        style={
                            'width': '60%',
                            'display': 'inline-block',
                        }
                    ),

                    html.Div(
                        [
                            html.Div(
                                id='details-label',
                                children='Nakieruj kursor na dowolne województwo aby zobaczyć szczegóły'
                            ),

                            dcc.Graph(
                                id='voivodeship-details',
                                style={
                                    'height': '100%',
                                    'width': '100%',
                                    "display": "block",
                                    "margin-left": "auto",
                                    "margin-right": "auto",
                                },
                            ),
                        ],
                        style={
                            'width': '40%',
                            'float': 'right',
                            'display': 'inline-block',
                        }
                    )
                ]),
        ],
        style={
            'margin-top': '30px',
            'textAlign': 'center',
        }
    )

    return layout
