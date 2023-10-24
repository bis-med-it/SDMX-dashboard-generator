"""Module providing generic utilities"""
import re
import dash_bootstrap_components as dbc
from dash import html
from schema import Schema, And, Or, Optional, SchemaError


def snake_case(string: str) -> str:
    """snake_case returns snake cased string

    :param string: str: input to be snake cased
    :returns: the input string snake cased

    """

    return "_".join(
        re.sub(
            "([A-Z][a-z]+)",
            r" \1",
            re.sub("([A-Z]+)", r" \1", string.replace("-", " ")),
        ).split()
    ).lower()


CLEANR = re.compile("<.*?>")


def cleanhtml(raw_html):
    """Clean raw html

    :param raw_html: str: the input to clean
    :returns: str: the cleaned text

    """
    cleantext = re.sub(CLEANR, "", raw_html)
    return cleantext


def get_label(names: list, data: list):
    """get label returns the label for the value in a list of dictionaries

    Args:
        names (list): _description_
        data (list): _description_

    Returns:
        list: a list with the matched pairs
    """
    ret_list = []
    for name in names:
        for val in data:
            if val["value"] == name:
                result = {"label": val["label"], "value": val["value"]}
                ret_list.append(result)
    return ret_list


def error_box(error: str, e: str = None):
    """error_box returns a html component with the error box

    Args:
        error (str): the error message
        e (str, optional): the KeyError. Defaults to None.

    Returns:
        _type_: a html component with the error box
    """
    if e:
        msg = f"{error}{e}"
    else:
        msg = error
    return dbc.Col(
        html.Div(
            [
                html.P(html.I(className="bi bi-emoji-frown h1")),
                html.Br(),
                html.P(str(msg)),
            ],
            style={"textAlign": "center"},
        )
    )


valid_schema_title_footer = Schema(
    {
        "Row": And(int),
        "chartType": And(str),
        "Title": And(str),
        Optional("Subtitle"): And(str),
    }
)

valid_schema_generic = Schema(
    {
        "Row": And(int),
        "chartType": And(str),
        "Title": And(Or(str, None)),
        "Unit": And(Or(str, None)),
        "legendConcept": And(Or(str, None)),
        "xAxisConcept": And(Or(str)),
        "yAxisConcept": And(Or(str)),
        "metadataLink": And(Or(str, None)),
        "DATA": And(Or(str, None)),
        Optional("Subtitle"): And(Or(str, None)),
        Optional("UnitShow"): And(Or(str, None)),
        Optional("UnitIcon"): And(Or(str, None)),
        Optional("unitLoc"): And(Or(str, None)),
        Optional("Decimals"): And(Or(int, None)),
        Optional("LabelsYN"): And(Or(str, bool, None)),
        Optional("downloadYN"): And(Or(str, bool, None)),
        Optional("legendLoc"): And(Or(str, None)),
        Optional("dataLink"): And(Or(str, None)),
        Optional("dsdLink"): And(Or(str, None)),
    }
)


def validate_yamlfile(file):
    """validate_yamlfile raises a SchemaError if the YAML is not valid

    Args:
        file (_type_): the YAML file

    Raises:
        se_ft: title or footer are not valid
        se: generic element is not valid
    """

    elements_t_f = [d for d in file["Rows"] if d["Row"] == 0]
    for element_t_f in elements_t_f:
        try:
            valid_schema_title_footer.validate(element_t_f)
        except SchemaError as se_ft:
            return se_ft

    elements_generic = [d for d in file["Rows"] if d["Row"] != 0]
    for element_generic in elements_generic:
        try:
            valid_schema_generic.validate(element_generic)
            return None
        except SchemaError as error:
            return error
