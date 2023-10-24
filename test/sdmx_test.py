from src.sdmx import get_components

endpoint_ilo = "https://www.ilo.org/sdmx/rest"
metadata_url = endpoint_ilo + "/dataflow/ILO/DF_POP_XWAP_SEX_AGE_NB/1.0?detail=full"


def _assert_metadata_not_empty(metadata):
    """
    Check that metadata components are correctly requested.

    Args:
        metadata (dict): metadata to be tested
    """
    assert isinstance(metadata, dict)


def test_get_metadata():
    """
    Test that metadata are correctly retrieved for
    ILO API url
    """
    metadata = get_components(metadata_url)
    _assert_metadata_not_empty(metadata)
