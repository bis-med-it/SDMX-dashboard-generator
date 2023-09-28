from src.app import download_data, load_yamlfile


def _assert_charts_not_empty(charts_per_r):
    """
    Check that data and metadata for graphs are correctly collected.

    Args:
        charts_per_r (list): the output of download_data(settings, value)
    """
    assert isinstance(charts_per_r, list)
    for row in charts_per_r:
        assert isinstance(row, list)
        for chart in row:
            assert isinstance(chart, dict)
            assert chart["data"] is not None
            assert chart["metadata_dataflow"] is not None
            assert chart["metadata_codelist"] is not None


def test_load_yaml_eurostat_sample():
    """
    Test that data and metadata are correctly retrieved for
    eurostat sample yaml file
    """
    fpath = "yaml/eurostat_sample.yaml"
    settings = load_yamlfile(fpath)
    charts_per_r, footer, value, spinner = download_data(settings, 2)
    _assert_charts_not_empty(charts_per_r)


def test_load_yaml_ilo_sample():
    """
    Test that data and metadata are correctly retrieved for
    ilo sample yaml file
    """
    fpath = "yaml/ilo_sample.yaml"
    settings = load_yamlfile(fpath)
    charts_per_r, footer, value, spinner = download_data(settings, 2)
    _assert_charts_not_empty(charts_per_r)
