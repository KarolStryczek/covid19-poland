import pandas as pd
from acquisition_app import MinistryOfHealthTwitter
from acquisition_app import ParserUtil
from visualization_app import AppUtil, callbacks
import json

voivodeship_ids = {"mazowieckie": 14, "wielkopolskie": 3, "małopolskie": 10, "dolnośląskie": 8, "zachodniopomorskie": 4,
                   "pomorskie": 11, "kujawsko-pomorskie": 6, "łódzkie": 13, "warmińsko-mazurskie": 12, "lubelskie": 15,
                   "śląskie": 1, "podkarpackie": 9, "opolskie": 2, "podlaskie": 7, "lubuskie": 16, "świętokrzyskie": 5}

geo_json = voivodeships = json.load(open('visualization_app/voivodeships.json', 'r', encoding='utf-8'))


def test_tweet_parsing_all_voivodeships() -> None:
    tweet_message = "Mamy 15 002 nowe i potwierdzone przypadki zakażenia #koronawirus z województw: " \
                    "mazowieckiego (2295), wielkopolskiego (1899), małopolskiego (1401), dolnośląskiego (1035), " \
                    "zachodniopomorskiego (965), pomorskiego (959), kujawsko-pomorskiego (931), łódzkiego (906), " \
                    "warmińsko-mazurskiego (864), lubelskiego (795), śląskiego (694), podkarpackiego (540), " \
                    "opolskiego (493), podlaskiego (455), lubuskiego (406), świętokrzyskiego (364)."

    expected_result_dict = {"mazowieckie": 2295, "wielkopolskie": 1899, "małopolskie": 1401, "dolnośląskie": 1035,
                            "zachodniopomorskie": 965, "pomorskie": 959, "kujawsko-pomorskie": 931, "łódzkie": 906,
                            "warmińsko-mazurskie": 864, "lubelskie": 795, "śląskie": 694, "podkarpackie": 540,
                            "opolskie": 493, "podlaskie": 455, "lubuskie": 406, "świętokrzyskie": 364}

    result = ParserUtil.parse_tweet_text(tweet_message)
    assert type(result) == pd.DataFrame

    for k, v in expected_result_dict.items():
        assert result[result['voivodeship'] == k]['cases'].values[0] == v


def test_tweet_parsing_selected_voivodeships() -> None:
    tweet_message = "Mamy 15 002 nowe i potwierdzone przypadki zakażenia #koronawirus z województw: " \
                    "mazowieckiego (2295), wielkopolskiego (1899), dolnośląskiego (1035), " \
                    "pomorskiego (959), kujawsko-pomorskiego (931), łódzkiego (906), " \
                    "śląskiego (694), podkarpackiego (540), podlaskiego (455), świętokrzyskiego (364)."

    expected_result_dict = {"mazowieckie": 2295, "wielkopolskie": 1899, "małopolskie": 0, "dolnośląskie": 1035,
                            "zachodniopomorskie": 0, "pomorskie": 959, "kujawsko-pomorskie": 931, "łódzkie": 906,
                            "warmińsko-mazurskie": 0, "lubelskie": 0, "śląskie": 694, "podkarpackie": 540,
                            "opolskie": 0, "podlaskie": 455, "lubuskie": 0, "świętokrzyskie": 364}

    result = ParserUtil.parse_tweet_text(tweet_message)
    assert type(result) == pd.DataFrame

    for k, v in expected_result_dict.items():
        assert result[result['voivodeship'] == k]['cases'].values[0] == v


def test_tweet_parsing_nonexistent_voivodeships() -> None:
    tweet_message = "Mamy 15 002 nowe i potwierdzone przypadki zakażenia #koronawirus z województw: " \
                    "nieistniejące-województwo (300)."

    result = ParserUtil.parse_tweet_text(tweet_message)
    assert sum(result.cases.values) == 0


def test_matching_tweet_pattern_correct_1() -> None:
    tweet_message = "Mamy 15 002 nowe i potwierdzone przypadki zakażenia #koronawirus z województw: " \
                    "mazowieckiego (2295), wielkopolskiego (1899), małopolskiego (1401), dolnośląskiego (1035), " \
                    "zachodniopomorskiego (965), pomorskiego (959), kujawsko-pomorskiego (931), łódzkiego (906), " \
                    "warmińsko-mazurskiego (864), lubelskiego (795), śląskiego (694), podkarpackiego (540), " \
                    "opolskiego (493), podlaskiego (455), lubuskiego (406), świętokrzyskiego (364)."

    twitter = MinistryOfHealthTwitter.MinistryOfHealthTwitter()
    assert twitter.match_tweet_text_to_pattern(tweet_message)


def test_matching_tweet_pattern_correct_2() -> None:
    tweet_message = "Mamy 11 497 nowych i potwierdzonych przypadków zakażenia #koronawirus z województw: " \
                    "mazowieckiego (1522), kujawsko-pomorskiego (1083), wielkopolskiego (1032), śląskiego (993), " \
                    "zachodniopomorskiego (973), pomorskiego (752), lubelskiego (745), warmińsko-mazurskiego (736), " \
                    "dolnośląskiego (698), łódzkiego (695), podkarpackiego (525), małopolskiego (404), " \
                    "lubuskiego (373), podlaskiego (356), opolskiego (315), świętokrzyskiego (183)"

    twitter = MinistryOfHealthTwitter.MinistryOfHealthTwitter()
    assert twitter.match_tweet_text_to_pattern(tweet_message)


def test_matching_tweet_pattern_correct_3() -> None:
    tweet_message = "Mamy 1 nowy i potwierdzony przypadek zakażenia #koronawirus z województw: " \
                    "mazowieckiego (1)."

    twitter = MinistryOfHealthTwitter.MinistryOfHealthTwitter()
    assert twitter.match_tweet_text_to_pattern(tweet_message)


def test_matching_tweet_pattern_wrong() -> None:
    tweet_message = "This is not even close to covid tweet pattern."

    twitter = MinistryOfHealthTwitter.MinistryOfHealthTwitter()
    assert not twitter.match_tweet_text_to_pattern(tweet_message)


def test_matching_tweet_empty() -> None:
    tweet_message = ""

    twitter = MinistryOfHealthTwitter.MinistryOfHealthTwitter()
    assert not twitter.match_tweet_text_to_pattern(tweet_message)


example_cases = [["mazowieckie", 2295],
                 ["wielkopolskie", 1899],
                 ["małopolskie", 0],
                 ["dolnośląskie", 1035],
                 ["zachodniopomorskie", 0],
                 ["pomorskie", 959],
                 ["kujawsko-pomorskie", 931],
                 ["łódzkie", 906],
                 ["warmińsko-mazurskie", 0],
                 ["lubelskie", 0],
                 ["śląskie", 694],
                 ["podkarpackie", 540],
                 ["opolskie", 0],
                 ["podlaskie", 455],
                 ["lubuskie", 0],
                 ["świętokrzyskie", 364]]


def test_populate_with_ids() -> None:
    cases_dataframe = pd.DataFrame(example_cases, columns=['voivodeship', 'cases'])

    expected_cases = [[r[0], r[1], voivodeship_ids[r[0]]] for r in example_cases]
    expected_dataframe = pd.DataFrame(expected_cases, columns=['voivodeship', 'cases', 'id'])

    result = AppUtil.populate_cases_with_ids(cases_dataframe, voivodeship_ids)
    assert type(result) == pd.DataFrame

    pd.testing.assert_frame_equal(expected_dataframe, result)


def test_map() -> None:
    cases_with_id = [[r[0], r[1], voivodeship_ids[r[0]]] for r in example_cases]
    cases_with_id_dataframe = pd.DataFrame(cases_with_id, columns=['voivodeship', 'cases', 'id'])

    cases_map = callbacks.prepare_choropleth_map_from_cases(cases_with_id_dataframe, voivodeship_ids)
    for i in range(len(example_cases)):
        id = cases_map.data[0].locations[i]
        name = None
        for k, v in voivodeship_ids.items():
            if v == id:
                name = k
        map_data = cases_map.data[0].z[i]
        assert map_data == example_cases[i][1]
        assert name == example_cases[i][0]


def test_details_graph() -> None:
    pass
