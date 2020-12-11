import dash_core_components as dcc
import dash_html_components as html
from visualization_app import AppUtil
import datetime as dt
from visualization_app import callbacks


def prepare_layout():
    layout = html.Div(
        [
            dcc.Tabs(id='page-tabs', value='tab-1', children=[
                dcc.Tab(label='Najnowsze zakażenia', value='tab-1'),
                dcc.Tab(label='Historia zakażeń', value='tab-2'),
            ]),
            html.Div(
                id='page-content',
                style={
                    'margin-top': '20px'
                }
            ),
        ],
        style={
            'textAlign': 'center',
        }
    )
    return layout


def page_1():
    new_date = max(AppUtil.get_dates())
    cases, voivodeships = AppUtil.get_cases_and_voivodeships(new_date, new_date)
    choropleth_map = callbacks.prepare_choropleth_map_from_cases(cases, voivodeships)
    cases_n = AppUtil.count_cases(cases)
    cases_word = "przypadek" if cases_n == 1 else "przypadki" if cases_n%10 in [2, 3, 4] else "przypadków"
    message = f'{new_date} ({cases_n} {cases_word})'
    return [
        html.H1(children="Najnowsze przypadki COVID-19"),
        html.H2(children=message),
        dcc.Graph(
            id='new-cases-map',
            figure=choropleth_map,
            style={
                'height': '700px',
                'width': 'auto',
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
            }
        )
    ]


def page_2():
    dates = AppUtil.get_dates()
    date_min, date_max = min(dates), max(dates)
    date_max_next_day = dt.datetime.strptime(date_max, '%Y-%m-%d') + dt.timedelta(days=1)
    date_month_before_max = dt.datetime.strptime(date_max, '%Y-%m-%d') - dt.timedelta(days=30)

    return [
        html.H1(children='Zachorowania na COVID-19'),

        html.Div(children='Poniższa mapa pokazuje nowe zachorowania w zadanym okresie'),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='cases-map',
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
                                minimum_nights=1,
                                with_portal=True,
                                min_date_allowed=date_min,
                                max_date_allowed=date_max_next_day,
                                initial_visible_month=date_max,
                                start_date=date_month_before_max,
                                end_date=date_max
                            ),
                        ),
                    ],
                    style={
                        'width': '45%',
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
                        'width': '55%',
                        'float': 'right',
                        'display': 'inline-block',
                    }
                )
            ]
        )
    ]
