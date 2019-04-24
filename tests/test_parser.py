import timemap
import datetime

gmaps_sample = "./tests/gmaps_sample.json"
FILE_START = "2018-04-19T21:07:52.746000"
FILE_END = "2018-04-19T20:47:20.433000"


def test_parser_serialization():

    parser = timemap.ParserHelper()
    print(parser)


def test_settings_acquisition():

    parser = timemap.ParserHelper.default_args()
    settings = parser.settings(skip_undefined=True)

    print(settings)
    assert settings.filepath == "./.history.json"
    assert settings.start > datetime.date(2018, 1, 1)
    assert settings.end > datetime.date(2018, 1, 6)
    assert settings.latitude > 61
    assert settings.longitude > 23
    assert settings.breaks > 0
    assert settings.radius > 100


if __name__ == "__main__":
    test_settings_acquisition()
