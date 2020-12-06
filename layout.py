import dash_core_components as dcc
import dash_html_components as html
import AppUtil

dates = AppUtil.get_dates()
date_min, date_max = min(dates), max(dates)


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
                                display_format='MM-D-Y',
                                minimum_nights=0,
                                min_date_allowed=date_min,
                                max_date_allowed=date_max,
                                initial_visible_month=date_max,
                                start_date=date_min,
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

