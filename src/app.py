"""application"""
import asyncio
import glob
import os
import platform
from itertools import islice

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import ALL, MATCH, Dash, Input, Output, State, callback, ctx, dcc, html
from dash.dash_table import DataTable
from dash.exceptions import PreventUpdate
from furl import furl

import yaml
from src.draw import ChartGenerator
from src.sdmx import (
    SDMXData,
    SDMXMetadata,
    get_components_async,
    get_translation,
    get_url_cl,
    translate_df,
    retreive_codes_from_data,
)
from src.utils import (
    snake_case,
    cleanhtml,
    error_box,
    validate_yamlfile,
)

external_stylesheets = [
    dbc.themes.COSMO,
    dbc.icons.FONT_AWESOME,
    dbc.icons.BOOTSTRAP,
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    prevent_initial_callbacks="initial_duplicate",
    suppress_callback_exceptions=True,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],
)

app.title = "SDMX Dashboard Generator"
application = app.server

dash.register_page("Home", layout="Home", path="/")

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.NavbarSimple(
            class_name="mb-3",
            brand="SDMX Dashboard Generator.\
                A web application for SMDX data and metadata rendering",
            color="primary",
            dark=True,
            children=[
                dbc.DropdownMenu(
                    label="Language",
                    children=[
                        dbc.DropdownMenuItem("English", id="en"),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Français", id="fr"),
                        dbc.DropdownMenuItem("Deutsch", id="de"),
                        dbc.DropdownMenuItem("Español", id="es"),
                    ],
                    direction="down",
                ),
                dbc.Button(
                    children=[html.I(className="fa fa-cog")],
                    id="collapse-button",
                    className="mb-3",
                    n_clicks=0,
                ),
                dbc.Button(
                    children=[html.I(className="bi bi-info-circle")],
                    id="open",
                    className="mb-3",
                    n_clicks=0,
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("SDMX Dashboard Generator")),
                        dbc.ModalBody(
                            [
                                html.Div(
                                    [
                                        html.B("SDMX Dashboard Generator"),
                                        " is an open-source Dash \
                            application that generates dynamic dashboards by\
                            pulling data and metadata from SDMX Rest API. \
                            It supports the version 2.1 of the standard.",
                                        html.Br(),
                                        html.Br(),
                                        "It leverages the open-source library SDMXthon\
                            to retrieve and parse data and metadata in SDMX.\
                            A dashboard is composed of several visualizations \
                            as defined by the specifications provided in \
                            a .yaml file stored in the /yaml folder.",
                                        html.Br(),
                                        html.Br(),
                                        "The full documentation is available at ",
                                        html.A(
                                            ["GitHub Pages"],
                                            href="https://urban-memory-73nlz2m.pages.github.io",
                                            target="_blank",
                                        ),
                                    ]
                                )
                            ]
                        ),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Close", id="close", className="ms-auto", n_clicks=0
                            )
                        ),
                    ],
                    id="modal",
                    is_open=False,
                ),
            ],
        ),
        dcc.Store(id="locale"),
        dcc.Store(id="yaml_file"),
        dcc.Store(id="settings"),
        dcc.Store(id="is_loaded"),
        dcc.Store(id="spinner"),
        dcc.Store(id="spinner2"),
        dcc.Store(id="get_data"),
        dcc.Store(id="get_data_complete"),
        dcc.Store(id="footer"),
        dbc.Container(
            [
                dbc.Collapse(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Upload(
                                id="upload-data",
                                children=html.Div(
                                    [
                                        "Drag and drop or ",
                                        html.A("select the configuration YAML file"),
                                    ]
                                ),
                                style={
                                    "width": "100%",
                                    "height": "60px",
                                    "lineHeight": "60px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin": "10px",
                                },
                                multiple=False,
                            ),
                        )
                    ),
                    id="collapse",
                    is_open=True,
                ),
                html.Div(id="title_div"),
                html.Div(
                    children=[
                        dcc.Loading(
                            id="loading-1",
                            type="default",
                            children=html.Div(id="spinner-id"),
                        )
                    ]
                ),
                html.Div(
                    children=[
                        dcc.Loading(
                            id="loading-2",
                            type="default",
                            children=html.Div(id="spinner-id2"),
                        )
                    ]
                ),
                dcc.Download(id="download_data"),
                html.Div(id="charts_div"),
                html.Div(id="footer_div"),
                html.Div(id="yaml_file_invalid"),
            ]
        ),
    ]
)


@callback(
    Output("locale", "data"),
    [
        Input("en", "n_clicks"),
        Input("fr", "n_clicks"),
        Input("de", "n_clicks"),
        Input("es", "n_clicks"),
    ],
)
def get_language(*args):
    """get_language returns the language code as returned by the callback

    :param *args: the language code clicked in the dropdown
    :returns: string with the language code requested which is cached

    """

    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "en"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    return button_id


@callback(
    Output("collapse", "is_open"),
    Input("collapse-button", "n_clicks"),
    Input("is_loaded", "data"),
    [State("collapse", "is_open")],
    prevent_initial_call=True,
)
def toggle_collapse(n: int, is_open: bool, is_loaded: bool):
    """toggle_collapse returns a boolean that contols the behaviour of the toggle menu
    of the settings

    :param n: int: the cumulative number of clicks since the start of the session
    :param is_open: bool: whether the toggle menu is open
    :param is_loaded: bool: whether the settings are loaded
    :returns: a boolean to control the behaviour of the toggle menu of the settings

    """

    if is_loaded:
        is_open = False
    elif n:
        is_open = True
    return is_open


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(open_clicks: int, close_clicks: int, is_open: bool):
    """toggle_collapse returns a boolean that contol the behaviour of the modal (Info)

    :param open_clicks: int: the cumulative number of clicks to open the modal
    :param close_clicks: int: the cumulative number of clicks to close the modal
    :param is_open: bool: whether the modal is open
    :returns: a boolean that contol the behaviour of the modal (Info)

    """

    if open_clicks or close_clicks:
        return not is_open
    return is_open


def load_yamlfile(filename: str, folder: str = None) -> dict:
    """load_yamlfile returns the loaded settings from the YAML file

    :param filename: str: the YAML file
    :param folder: str, optional: the YAML file folder location
    :returns: a dictionary with loaded settings from the YAML file

    """

    try:
        path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        if folder:
            fpath = os.path.join(path, folder, filename)
        else:
            fpath = os.path.join(path, filename)

        with open(fpath, encoding="utf-8") as f:
            settings = yaml.safe_load(f)
            return settings

    except yaml.YAMLError as exc:
        print(exc)

    except Exception as e:
        print(e)
        raise PreventUpdate from e


@callback(
    Output("yaml_file", "data"), [Input("url", "href")], prevent_initial_call=True
)
def load_yaml(href: str):
    """load_yaml returns the location of the YAML file whose dashID matches
    the string provided in the href of the URL

    :param href: str: the dashID
    :returns: a string with the location of the requested YAML file

    """

    try:
        files = glob.glob(r"yaml/*.yaml")
        yaml_files = []

        for file in files:
            yaml_content = load_yamlfile(file)
            dash_file_map = {"dash_id": yaml_content["DashID"], "location": file}
            yaml_files.append(dash_file_map)

        f = furl(href)
        dash_id_url = str(f.path)
        dash_id_url_s = "".join(dash_id_url.split("/", 1))

        if dash_id_url == "/":
            raise PreventUpdate

        yaml_location = "".join(
            [d["location"] for d in yaml_files if d["dash_id"] == dash_id_url_s]
        )
        return yaml_location

    except Exception as e:
        print(e)


@callback(
    Output("settings", "data", allow_duplicate=True),
    Output("is_loaded", "data", allow_duplicate=True),
    Output("yaml_file_invalid", "children", allow_duplicate=True),
    [Input("yaml_file", "data")],
    prevent_initial_call=True,
)
def load_content(yaml_file):
    """load_content returns a dictionary with the settings from the YAML file
    and a boolean on whether the settings are loaded

    :param yaml_file: the relative path of the YAML file
    :returns: a dictionary with the settings and a boolean when the loading is completed

    """

    try:
        if yaml_file is None:
            raise PreventUpdate
        data = load_yamlfile(yaml_file)
        validation = validate_yamlfile(data)
        if validation:
            out = None, None, error_box(f"Invalid YAML file. Error:{validation.code}")
        else:
            is_loaded = True
            out = data, is_loaded, ""
        return out

    except Exception as e:
        print(e)
        raise PreventUpdate from e


@callback(
    Output("url", "pathname"), Input("settings", "data"), prevent_initial_call=True
)
def get_dash_id(i):
    """get_dash_id returns the snake cased DashID from the YAML file settings

    :param i: a dictionary with settings from the YAML file
    :returns: a string with the snaked cased DashId

    """
    if i is None:
        raise PreventUpdate

    try:
        return snake_case(i["DashID"])
    except Exception as e:
        print(e)
        return str(e)


def get_title_footer(data):
    """get_title_footer returns a dictionary with entries with Row == 0
    specified in the YAML file

    :param data: a dictionary with settings from the YAML file
    :returns: a dictionary with the title and footer, or any other entry
              with Row == 0 in the YAML file

    """
    try:
        dash_title_footer = [d for d in data if d["Row"] == 0]
        return dash_title_footer
    except Exception as e:
        print(e)


def generate_title(data, key: str):
    """generate_title returns the title from the YAML file

    :param data: a dictionary with settings from the YAML file
    :param key: str: the key (TITLE) from settings from the YAML file
    :returns: a html.Span with the title of the dashboard as specified in the YAML file

    """
    try:
        dash_title_footer = get_title_footer(data)
        element1 = "".join(
            [d["Title"] for d in dash_title_footer if d["chartType"] == key]
        )
        element2 = "".join(
            [d["Subtitle"] for d in dash_title_footer if d["chartType"] == key]
        )
        if element2:
            element = html.Span(
                [
                    html.Br(),
                    html.Br(),
                    html.H1(element1, style={"textAlign": "center"}),
                    html.H4(element2, style={"textAlign": "center"}),
                    html.Br(),
                ]
            )
        else:
            element = html.Span(
                [
                    html.Br(),
                    html.Br(),
                    html.H1(element1, style={"textAlign": "center"}),
                    html.Br(),
                ]
            )
        return element

    except Exception as e:
        print(e)
        return str(e)


def generate_footer(data, key: str):
    """generate_footer returns the footer from the YAML file

    :param data: a dictionary with settings from the YAML file
    :param key: str: the key (FOOTER) from settings from the YAML file
    :returns: a html.Span with the footer of the dashboard as specified in the YAML file

    """
    try:
        dash_title_footer = get_title_footer(data)
        element1 = "".join(
            [d["Title"] for d in dash_title_footer if d["chartType"] == key]
        )
        element2 = "".join(
            [d["Subtitle"] for d in dash_title_footer if d["chartType"] == key]
        )
        if element2:
            element = html.Span(
                [
                    html.Br(),
                    html.Br(),
                    html.H6(
                        element1, style={"textAlign": "center", "font-size": "8px"}
                    ),
                    html.H6(
                        element2, style={"textAlign": "center", "font-size": "8px"}
                    ),
                ]
            )
        else:
            element = html.Span(
                [
                    html.Br(),
                    html.Br(),
                    html.H1(element1, style={"textAlign": "center"}),
                    html.Br(),
                ]
            )
        return element

    except Exception as e:
        print(e)
        return str(e)


@callback(
    Output("title_div", "children"),
    Output("spinner", "data"),
    Input("settings", "data"),
    prevent_initial_call=True,
)
def get_dashboard_title(data):
    """get_dashboard_title returns the title to the dashboard and controls
    the behaviour of the loading spinner

    :param data: a dictionary with settings from the YAML file
    :returns: a html.Span with the title of the dashboard and an integer
              that controls the behaviour of the loading spinner

    """
    if data is None:
        raise PreventUpdate
    try:
        title = generate_title(data["Rows"], key="TITLE")
        spinner = ""
        return title, spinner

    except Exception as e:
        print(e)
        return str(e)


def get_text_kpi(kpi, code, chart):
    """Build text to show for kpi

    :param kpi: the ChartGenerator kpi object
    :param code: the code of the element
    :param chart: the chart settings
    :returns: the html element with the kpi text

    """
    try:
        unit_show = chart["UnitShow"]

    except Exception as e:
        print(e)
        unit_show = None

    if unit_show == "Yes":
        out = html.P(
            [
                html.H2(
                    [str(kpi[code][1]) + " " + chart["Unit"]],
                    className="card-title",
                    style={"text-align": "center"},
                )
            ]
        )

    else:
        out = html.P(
            [
                html.H2(
                    [str(kpi[code][1])],
                    className="card-title",
                    style={"text-align": "center"},
                )
            ]
        )
    return out


def get_icon_kpi(kpi, code, chart):
    """Build icon for kpi if available

    :param kpi: The ChartGenerator kpi object
    :param code: the code of the element
    :param chart: The chart settings
    :returns: The html element containing the kpi icon

    """
    try:
        unit_icon = chart["UnitIcon"]

    except Exception as e:
        print(e)
        unit_icon = None

    if unit_icon:
        out = [
            html.P(html.I(className=unit_icon), style={"text-align": "center"}),
            html.H5(
                str(kpi[code][0]),
                className="card-title",
                style={"text-align": "center"},
            ),
            get_text_kpi(kpi, code, chart),
        ]

    else:
        out = [
            html.H5(
                str(kpi[code][0]),
                className="card-title",
                style={"text-align": "center"},
            ),
            get_text_kpi(kpi, code, chart),
        ]
    return out


def draw_chart(df, chart):
    """Draw the chart

    :param df: the pandas.DataFrame containing data
    :param chart: the chart settings loaded from the yaml file
    :raises ValueError: in case x or y axis is not specified.
    :returns: the html element containing the graph

    """
    error_message = "Error in fetching the data, please check the YAML file: "

    if chart["xAxisConcept"] is None or chart["yAxisConcept"] is None:
        raise ValueError("Please provide xAxisConcept")

    chart_type = chart["chartType"]

    config = {"displayModeBar": False}

    if df.empty or not isinstance(df, pd.DataFrame):
        return error_box("Data is empty. Please check the YAML file")

    if chart_type == "VALUE":
        try:
            kpi = ChartGenerator().calculate_kpi(
                df,
                yAxisConcept=chart["yAxisConcept"],
                xAxisConcept=chart["xAxisConcept"],
                legendConcept=chart["legendConcept"],
                decimals=chart["Decimals"],
            )
            code = list(kpi.keys())[0]

            return dbc.Col(
                dbc.CardBody(
                    get_icon_kpi(kpi, code, chart),
                    className="shadow-lg p-3 mb-5 bg-transparent rounded",
                )
            )

        except Exception as e:
            return error_box("Something went wrong. Please check the YAML file: ", e)

    else:
        try:
            if chart_type == "PIE":
                fig = ChartGenerator().pie_chart(
                    df,
                    yAxisConcept=chart["yAxisConcept"],
                    xAxisConcept=chart["xAxisConcept"],
                    legendLoc=chart["legendLoc"],
                    LabelsYN=chart["LabelsYN"],
                )

            elif chart_type == "BAR":
                fig = ChartGenerator().bar_chart(
                    df,
                    yAxisConcept=chart["yAxisConcept"],
                    xAxisConcept=chart["xAxisConcept"],
                    color=chart["legendConcept"],
                    legendLoc=chart["legendLoc"],
                )

            else:
                fig = ChartGenerator().time_series_chart(
                    df,
                    yAxisConcept=chart["yAxisConcept"],
                    xAxisConcept=chart["xAxisConcept"],
                    color=chart["legendConcept"],
                    legendLoc=chart["legendLoc"],
                )

            return dbc.Col(
                html.Div(
                    dbc.CardBody(
                        dcc.Graph(figure=fig, config=config),
                        className="shadow-lg p-3 mb-5 bg-transparent rounded",
                    )
                ),
                align="start",
            )

        except Exception as e:
            return dbc.Col(
                html.Div(dbc.CardBody([html.P(str(error_message + str(e)))]))
            )


@callback(
    Output({"type": "off-canvas", "index": MATCH}, "is_open"),
    Input({"type": "list-item", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def open_metadata_offcanvas(click):
    """Open metadata offcanvas on click if closed"""
    open_offcanvas = bool(click)
    return open_offcanvas


def create_info_button(chart_id):
    """Create chart info button

    :param chart_id: reference chart
    :returns: html element with the info button

    """
    return html.Span(
        html.I(className="bi bi-info-circle-fill", id=chart_id),
        n_clicks=0,
        style={"cursor": "pointer"},
        id="open-offcanvas",
    )


def create_table_button(chart_id):
    """Create chart table button

    :param chart_id: reference chart
    :returns: html element with the table button

    """
    return html.Span(
        html.I(className="bi bi-table", id=chart_id),
        n_clicks=0,
        style={"cursor": "pointer"},
    )


def create_download_button(chart_id):
    """Create chart download button

    :param chart_id: reference chart
    :returns: html element with the download button

    """
    return html.Span(
        html.I(
            className="bi bi-download", id={"type": "list-download", "index": chart_id}
        ),
        n_clicks=0,
        style={"cursor": "pointer"},
    )


def get_dataflow_metadata(data, meta):
    """Create metadata element and fall back on data title

    :param data: the chart data structure
    :param meta: the metadata
    :returns: html element with metadata or title

    """
    if meta:
        if meta[1]:
            return html.Div(
                [html.H2(meta[0]), html.Div(children=[html.P([cleanhtml(meta[1])])])]
            )
        if meta[0]:
            return html.Div([html.H2(meta[0])])
    else:
        try:
            return dbc.CardHeader(data["Title"])
        except Exception as e:
            print(e)


def create_offcanvas(data, chart_id, df_metadata):
    """Create metadata (info) offcanvas

    :param data: the chart datastructure
    :param chart_id: reference chart
    :param df_metadata: metadata for the chart
    :returns: the offcanvas element shown on info button click

    """
    try:
        return html.Div(
            [
                dbc.Offcanvas(
                    [get_dataflow_metadata(data, df_metadata)],
                    id={"type": "off-canvas", "index": chart_id},
                    is_open=False,
                    scrollable=True,
                )
            ]
        )
    except Exception as e:
        print(e)
        return html.Div(data["Title"])


@callback(
    Output({"type": "off-canvas2", "index": MATCH}, "is_open"),
    Input({"type": "list-item2", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def open_table_offcanvas(click):
    """Open table offcanvas on click if closed"""
    open_offcanvas = bool(click)
    return open_offcanvas


def create_download(chart_id):
    """Create the download section of the offcanvas

    :param chart_id: reference chart
    :returns: dashboard component with download section

    """
    listgroup_item_down = dbc.ListGroupItem(
        [
            html.P(
                [
                    "Click the icon to download the table :",
                    html.Br(),
                    create_download_button(chart_id),
                ],
                n_clicks=0,
            )
        ],
        id={"type": "list-download", "index": chart_id},
        n_clicks=0,
        className="border-0 text-nowrap list-group-item-action",
    )

    toast = dbc.Col(
        [
            html.Div(
                [
                    dbc.Toast(
                        [html.P(listgroup_item_down, className="mb-0")],
                        header="Download",
                    )
                ]
            )
        ]
    )

    return toast


def create_filter_dropdown(df: pd.DataFrame, concept: str, chart_id: str, valuelist):
    """update_filter_output updates the filter dropdown for the data

    Args:
        n_clicks: the clicks on the filter dropdown
        data: a pd.DataFrame with the data without any fikter applied

    Returns:
        data: a dictionary with the data filtered

    """
    try:
        if len(valuelist) > 1:
            try:
                lst_value = list(set(list(df[concept + "_id"])))

                return html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        valuelist,
                                        lst_value,
                                        multi=True,
                                        id={"type": "list-dropdown", "index": chart_id},
                                    ),
                                    width=9,
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "OK",
                                        id={
                                            "type": "list-dropdown-btn",
                                            "index": chart_id,
                                        },
                                        n_clicks=0,
                                        size="sm",
                                    ),
                                    width=1,
                                ),
                            ]
                        )
                    ]
                )

            except Exception:
                return html.Div("")
        else:
            return html.Div("")

    except Exception:
        return html.Div("")


@callback(
    Output("get_data", "data", allow_duplicate=True),
    Input({"type": "list-dropdown-btn", "index": ALL}, "n_clicks"),
    Input("get_data_complete", "data"),
    State({"type": "list-dropdown", "index": ALL}, "value"),
    prevent_initial_call=True,
)
def update_output(n_clicks, data):
    """create_filter_dropdown creates the filter dropdown for the data

    Args:
        df: pd.DataFrame containg the data
        concept: the legendConcept as specified in the YAML file
        chart_id: the chart ID
        valuelist: the valuelist containing the unique values of the legendConcept

    Returns:
        html.Div: a dcc.Dropdown and a dbc.Button containing the values to filter

    """
    if sum(filter(None, n_clicks)) == 0:
        raise PreventUpdate

    chart_id = ctx.triggered_id.index
    row = int(chart_id[0])
    pos = int(chart_id[1])
    states_list = ctx.states_list[0]
    val = [i["value"] for i in states_list if i["id"]["index"] == chart_id][0]

    legendConcept = data[row][pos]["settings"]["legendConcept"]
    df = pd.DataFrame(data[row][pos]["data"])
    df_filtered = df.loc[df[legendConcept].isin(val)]
    data[row][pos]["data"] = df_filtered.to_dict("records")

    return data


def create_offcanvas_table(data, chart_id, df, valuelist):
    """Create the table offcanvas element of the dashboard.
    The structure depends on whether the data can be downloaded or not.

    :param data: the chart data structure
    :param chart_id: reference chart
    :param df: the chart data
    :param valuelist: values for filtering
    :returns: the offcanvas element shown when the table button is clicked

    """
    try:
        # Check if the data has a "downloadYN" flag set to "Y" for enabling downloads.
        if data["downloadYN"] == "Yes":
            # Create an HTML strucesture with an off-canvas element for a chart
            # with download capability.
            out = html.Div(
                [
                    dbc.Offcanvas(
                        children=[
                            dbc.Row(
                                [
                                    # Create a column for displaying unit information
                                    # and source URL as toasts.
                                    dbc.Col(
                                        [
                                            create_toast(
                                                data=data["Unit"], header="Unit"
                                            ),
                                            create_toast(
                                                data=data["DATA"],
                                                header="Source URL",
                                                href=True,
                                            ),
                                            create_download(chart_id),
                                        ],
                                        align="start",
                                        width=3,
                                    ),
                                    # Create a column for displaying the table
                                    # associated with the chart.
                                    dbc.Col(
                                        [
                                            create_filter_dropdown(
                                                df,
                                                data["legendConcept"],
                                                chart_id,
                                                valuelist,
                                            ),
                                            html.Hr(className="my-2"),
                                            create_table(chart_id, df),
                                        ],
                                        id=chart_id,
                                        width=9,
                                    ),
                                ],
                                id=chart_id,
                            )
                        ],
                        id={"type": "off-canvas2", "index": chart_id},
                        is_open=False,
                        scrollable=True,
                        placement="bottom",
                        style={"height": "500px"},
                    )
                ]
            )
        else:
            # Create an HTML structure with an off-canvas element for a chart
            # without download capability.
            out = html.Div(
                [
                    dbc.Offcanvas(
                        children=[
                            dbc.Row(
                                [
                                    # Create a column for displaying unit information
                                    # and source URL as toasts.
                                    dbc.Col(
                                        [
                                            create_toast(data["Unit"], "Unit"),
                                            create_toast(data["DATA"], "Source URL"),
                                        ],
                                        align="center",
                                        width=3,
                                    ),
                                    # Create a column for displaying the table
                                    # associated with the chart.
                                    dbc.Col(
                                        [create_table(chart_id, df)],
                                        id=chart_id,
                                        width=9,
                                    ),
                                ]
                            )
                        ],
                        id={"type": "off-canvas2", "index": chart_id},
                        is_open=False,
                        scrollable=True,
                        placement="bottom",
                        style={"height": "500px"},
                    )
                ]
            )
        return out

    except Exception as e:
        # Handle exceptions and print the error message.
        print(e)
        return html.Div("")


@callback(
    Output("download_data", "data"),
    Input({"type": "list-download", "index": ALL}, "n_clicks"),
    State({"type": "data_table", "index": ALL}, "data"),
    prevent_initial_call=True,
)
def download_table(n_clicks, data):
    """download_table returns the export table in CSV.

    :param n_clicks: int: the number of times that the list-download
                          chart-id has been clicked on
    :param data: the DataTable returned by create_table()
    :returns: triggers dcc.send_data_frame to download the table as CSV

    """

    id_tag = ctx.triggered_id.index
    states_list = ctx.states_list[0]
    data = [i["value"] for i in states_list if i["id"]["index"] == id_tag][0]

    if sum(filter(None, n_clicks)) == 0:
        raise PreventUpdate

    df = pd.DataFrame(data)
    return dcc.send_data_frame(df.to_csv, "export_table.csv", index=False)


def create_table(chart_id: str, df: pd.DataFrame):
    """create_table returns the Dash DataTable to be displayed in the offcanvas
    and exported.

    :param chart_id: str: the unique chart ID which correspond to the row and the
                          sequential number (int) of the chart as specified in the YAML
    :param df: pd.DataFrame: the pd.DataFrame associated with the chart ID
    :returns: Dash DataTable

    """
    # Convert the DataFrame to a list of records and configure DataTable
    return DataTable(
        data=df.to_dict("records"),
        id={"type": "data_table", "index": chart_id},
        sort_action="native",
        style_table={"overflowX": "auto"},
        style_cell={"backgroundColor": "white", "color": "black"},
        style_header={
            "backgroundColor": "black",
            "color": "white",
            "fontWeight": "bold",
        }
        # editable=False  # Enable editing
        # row_deletable=False  # Enable row deletion
    )


def create_chart_item(
    data: dict, chart_id: str, df_metadata: list, df: pd.DataFrame, valuelist: list
):
    """create_chart_item returns the HTML div for the info and table buttons

    :param data: dict: the settings of the chart as specified in the YAML
    :param chart_id: str: the unique chart ID which correspond to the row and the
                          sequential number (int) of the chart as specified in the YAML
    :param df_metadata: list: the list of metadata associated with the chart
    :param df: pd.DataFrame: the DataFrame associated with the chart ID
    :returns: html.Div with the info and table buttons

    """

    # Create a list group item with an info button for displaying metadata.
    listgroup_item = dbc.ListGroupItem(
        [html.Div([create_info_button(chart_id)])],
        id={"type": "list-item", "index": chart_id},
        n_clicks=0,
        className="border-0 text-nowrap list-group-item-action",
    )

    # Create a list group item with a table button for displaying chart-related tables.
    listgroup_item_down = dbc.ListGroupItem(
        [html.Div([create_table_button(chart_id)])],
        id={"type": "list-item2", "index": chart_id},
        n_clicks=0,
        className="border-0 text-nowrap list-group-item-action",
    )

    # Check if metadata link exists and metadata is available.
    if (data["metadataLink"]) and (df_metadata):
        try:
            # Create a row with two columns: one for info button and off-canvas,
            # and another for table button and off-canvas.
            return dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            children=[
                                listgroup_item,
                                create_offcanvas(data, chart_id, df_metadata),
                            ]
                        )
                    ),
                    dbc.Col(
                        html.Div(
                            children=[
                                listgroup_item_down,
                                create_offcanvas_table(data, chart_id, df, valuelist),
                            ]
                        )
                    ),
                ]
            )
        except Exception as e:
            # Handle exceptions and print the error message.
            print(e)
            return html.Div([])
    else:
        try:
            # Create a row with a single column for the table button and off-canvas.
            return dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    listgroup_item_down,
                                    create_offcanvas_table(
                                        data, chart_id, df, valuelist
                                    ),
                                ]
                            )
                        ]
                    )
                ]
            )
        except Exception as e:
            # Handle exceptions and print the error message.
            print(e)
            return html.Div([])
    return html.Div([])


def create_toast(data, header: str, href=False):
    """create_toast returns the dbc.Toast with the statistic metadata set in the YAML

    :param data: the corresponding value of the chart as specified in the YAML
    :param header: str: the corresponding key associated to each chart in the YAML file
    :param href: bool: whether the text shall be encoded as link
    :returns: dbc.Toast with the statistic metadata,
              Unit and source (DATA) set in the YAML

    """
    if href:
        toast = dbc.Col(
            [
                html.Div(
                    [
                        dbc.Toast(
                            [
                                html.P(
                                    html.A(
                                        children=[str(data)],
                                        href=str(data),
                                        target="_blank",
                                    ),
                                    className="mb-0",
                                )
                            ],
                            header=header,
                        )
                    ]
                )
            ]
        )
    else:
        toast = dbc.Col(
            [
                html.Div(
                    [dbc.Toast([html.P(str(data), className="mb-0")], header=header)]
                )
            ]
        )
    return toast


def get_static_metatada(chart, chart_id, df_metadata, df, valuelist):
    """get_static_metatada returns the HTML div for the info and table buttons

    :param chart: the settings of the chart as specified in the YAML
    :param chart_id: the unique chart ID which correspond to the row and the sequential
                     number (int) of the chart as specified in the YAML
    :param df_metadata: the list of metadata associated with the chart
    :param df: the pd.DataFrame associated with the chart ID
    :returns: html.Div with the dbc.CardBody containing the title, subtitle and
              the buttons (table and info)

    """

    concept = chart["legendConcept"]
    title_default = str(chart["Title"])
    subtitle_default = str(chart["Subtitle"])

    if df_metadata:
        try:
            if title_default == "None" or title_default is None:
                title = str(df_metadata[0])
            else:
                title = title_default
        except Exception as e:
            print(e)
            title = title_default
        try:
            if subtitle_default == "None" or title_default is None:
                subtitle = ""
            elif subtitle_default == "auto":
                try:
                    subtitle = str(df[concept][0])
                    if len(set(df[concept + "_id"])) > 1:
                        subtitle = str(df[concept][0] + "...")
                    elif subtitle is None or subtitle == "None":
                        try:
                            if len(set(df[concept + "_id"])) > 0:
                                subtitle = str(df[concept + "_id"][0] + "...")
                            else:
                                subtitle = str(df[concept + "_id"][0])
                        except Exception as e:
                            print(e)
                            subtitle = ""
                except Exception as e:
                    print(e)
                    try:
                        subtitle = str(df[concept + "_id"][0])
                    except Exception as e_n:
                        print(e_n)
                        subtitle = ""
            else:
                subtitle = subtitle_default
        except Exception as e:
            print(e)
            subtitle = subtitle_default

    else:
        title = title_default
        subtitle = subtitle_default

    try:
        content = dbc.Col(
            html.Div(
                dbc.CardBody(
                    id=chart_id,
                    children=[
                        dbc.Row(
                            html.Div(
                                [
                                    html.H4(title, className="card-title"),
                                    html.Div(
                                        children=[
                                            html.P(
                                                [
                                                    subtitle,
                                                    create_chart_item(
                                                        chart,
                                                        chart_id,
                                                        df_metadata,
                                                        df,
                                                        valuelist,
                                                    ),
                                                ],
                                                id=chart_id,
                                            ),
                                            html.Hr(className="my-2"),
                                        ]
                                    ),
                                ]
                            ),
                            align="end",
                        )
                    ],
                )
            ),
            id=chart_id,
            style={"textAlign": "center"},
            align="end",
        )
    except Exception as e:
        content = dbc.Col(
            html.Div(
                dbc.CardBody(
                    id=chart_id,
                    children=[
                        dbc.Row(
                            html.Div(
                                [
                                    html.H2(title, className="card-title"),
                                    html.Div(
                                        children=[
                                            html.P(
                                                [
                                                    subtitle,
                                                    html.Div(["Error: " + str(e)]),
                                                ],
                                                id=chart_id,
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            align="end",
                        )
                    ],
                )
            ),
            id=chart_id,
            style={"textAlign": "center"},
            align="end",
        )

    return content


def get_rows(data: dict, max_charts_per_row: int = 3):
    """get_rows returns the distribution of the charts per row in the dashboard

    :param data: dict: the settings of the chart as specified in the YAML
    :param max_charts_per_row: int: the maximum charts per row (Default value = 3)
    :returns: list with the distribution of the charts per row

    """

    try:
        rows = list({i["Row"] for i in data})
        charts_per_row = []
        for row in rows:
            charts_in_row = [d for d in data if d["Row"] == row]
            if len(charts_in_row) > max_charts_per_row:
                charts_in_row = charts_in_row[:max_charts_per_row]
            charts_per_row.append(charts_in_row)
        return charts_per_row

    except Exception as e:
        print(e)


async def download_single_data_chart(chart_id, data, concept):
    """Download data for a single chart

    :param chart_id: the chart ID corresponding to row number and position in row
    :param data: the DATA link specified in the YAML file
    :param concept: the concept specified in the YAML file
    :returns: list of couroutines with downloaded data as pd.DataFrame

    """
    print("Getting data", chart_id)
    try:
        df = await SDMXData(data=data).get_data_async(yAxisConcept=concept)
    except Exception as e:
        print(
            f"There has been a problem in downloading data for {chart_id}. Error: {e}"
        )
        df = pd.DataFrame
    return df


async def download_single_chart(data_chart, row: int, pos: int):
    """Download data and metadata for a single chart

    :param data_chart: the settings of the single chart
    :param z: int: Row number
    :param y: int: Position in row
    :returns: dict with chart settings and data

    """
    chart_id = f"{row}{pos}"

    # Data
    task = asyncio.create_task(
        download_single_data_chart(
            chart_id, data_chart["DATA"], data_chart["yAxisConcept"]
        )
    )
    try:
        df = await asyncio.wait_for(task, timeout=30)

    except asyncio.exceptions.TimeoutError:
        df = pd.DataFrame()
        print(f"Data download for chart {chart_id} was cancelled due to a timeout")

    except Exception as e:
        df = pd.DataFrame()
        print(
            f"There has been a problem dowloading data for chart {chart_id}. Error:{e}"
        )

    print("Getting metadata", chart_id)
    concept = data_chart["legendConcept"]

    try:
        # If dsdLink is provided, this increases significantly the overall performance
        dsdLink = data_chart["dsdLink"]
        metadata_components = await get_components_async(
            url=data_chart["metadataLink"], descendants=False
        )
        metadata_dataflow = SDMXMetadata(
            components=metadata_components
        ).dataflow_metadata()

        if concept:
            components = await get_components_async(dsdLink, descendants=False)
            cl_name = SDMXMetadata(components, concept=concept).get_codelist_name()
            cl_url = get_url_cl(dsdLink, cl_name)
            cl_id_all = await get_components_async(cl_url, descendants=False)
            cl_id = cl_id_all["Codelists"][cl_name]
            metadata_codelist = retreive_codes_from_data(df, concept, cl_id)

        else:
            metadata_codelist = None

    # Fallback to descendants but less performant
    except Exception as e:
        print(
            f"Invalid dsdLink for {chart_id}. Falling back to dataflow with descendants. Error:{e}"
        )
        if data_chart["metadataLink"]:
            # Metadata
            try:
                metadata_components = await get_components_async(
                    url=data_chart["metadataLink"]
                )
                # Dataflow
                metadata_dataflow = SDMXMetadata(
                    components=metadata_components
                ).dataflow_metadata()
                # Codelist

                if concept:
                    cl_id = SDMXMetadata(
                        metadata_components, concept
                    ).get_codelist_name()

                    metadata_codelist = retreive_codes_from_data(df, concept, cl_id)

                else:
                    metadata_codelist = None

            except Exception as e_n:
                print(f"There has been an issue with the metadata. Error{e_n}")
                metadata_dataflow = {
                    "name": {"en": data_chart["Title"]},
                    "description": {
                        "en": str(
                            data_chart["Subtitle"]
                            + " Please provide a valid dataflow link\
                                to retreive the metadata"
                        )
                    },
                }
                metadata_codelist = None

        else:
            metadata_dataflow = {
                "name": {"en": data_chart["Title"]},
                "description": {
                    "en": str(data_chart["Subtitle"])
                    + " Please add a dataflow link in your configuration file\
                        to retreive the metadata"
                },
            }
            metadata_codelist = None

    result = {
        "chart_id": chart_id,
        "settings": data_chart,
        "data": df.to_dict("records") if df is not None else None,
        "valuelist": list(set(list(df[concept]))) if df is not None else None,
        "metadata_dataflow": metadata_dataflow,
        "metadata_codelist": metadata_codelist,
    }
    print("Done with", chart_id)
    return result


async def download_charts(chart_per_rows):
    """Download chart data asyncronously

    :param chart_per_rows: output of get_rows()
    :returns: chart data and metadata, split in row lists

    """
    all_cors = []
    row_lengths = []
    for row, chart in enumerate(chart_per_rows):
        data_charts = list(chart)
        row_lengths.append(len(data_charts))

        for pos, data_chart in enumerate(data_charts):
            cor = download_single_chart(data_chart, row, pos)
            all_cors.append(cor)

    all_charts = await asyncio.gather(*all_cors)
    all_charts = iter(all_charts)
    charts_per_r = [list(islice(all_charts, i)) for i in row_lengths]

    return charts_per_r


@callback(
    Output("get_data", "data"),
    Output("get_data_complete", "data"),
    Output("footer", "data"),
    Output("spinner-id", "children"),
    Output("spinner2", "data"),
    [Input("settings", "data")],
    Input("spinner", "data"),
    prevent_initial_call=True,
)
def download_data(settings, value):
    """download_data returns the cached data and the footer required to build the
    charts_div and footer_div

    :param settings: the settings of the chart as specified in the YAML
    :param value: any value that controls the behaviour of the spinner
    :returns: a dictionary with the cached data required to build the charts_div,
             the footer, the spinners 1 and 2

    """

    if settings is None:
        raise PreventUpdate

    if settings:
        charts = [d for d in settings["Rows"] if d["Row"] != 0]
        chart_per_rows = get_rows(charts)
        footer = generate_footer(settings["Rows"], key="FOOTER")

        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        charts_per_r = asyncio.run(download_charts(chart_per_rows))
        spinner = ""

        return charts_per_r, charts_per_r, footer, value, spinner


@callback(
    Output("charts_div", "children"),
    Output("footer_div", "children"),
    Output("spinner-id2", "children"),
    [Input("get_data", "data")],
    [Input("footer", "data")],
    [Input("locale", "data")],
    Input("spinner2", "data"),
    prevent_initial_call=True,
)
def add_graphs(data, footer, lang, value):
    """add_graphs returns the charts div in the dashboard page

    :param data: the cached data of the charts as returned by download_data
    :param footer: the footer div generated by download_data
    :param lang: the language selected in the dropdown
    :param value: anyvalue that controls the behaviour of the spinner
    :returns: html.Div with the charts loaded in the cache

    """

    global LANG
    LANG = lang

    if data is None:
        raise PreventUpdate

    if data:
        try:
            charts_per_r = []

            for data_per_row in data:
                graphs = []
                texts = []

                for data_per_row_pos in data_per_row:
                    chart_id = data_per_row_pos["chart_id"]
                    data_chart = data_per_row_pos["settings"]
                    df = pd.DataFrame(data_per_row_pos["data"])
                    valuelist = data_per_row_pos["valuelist"]
                    metadata_dataflow = data_per_row_pos["metadata_dataflow"]

                    try:
                        metadata_dataflow_translated = [
                            get_translation(metadata_dataflow[i], lang)
                            for i in list(metadata_dataflow.keys())
                        ]
                    except Exception as e:
                        print(e)

                    metadata_codelist = data_per_row_pos["metadata_codelist"]

                    if metadata_codelist:
                        try:
                            metadata_codelist_items_translated = {
                                i: get_translation(metadata_codelist["items"][i], lang)
                                for i in list(metadata_codelist["items"].keys())
                            }

                        except Exception as e:
                            metadata_codelist_items_translated = metadata_codelist
                            print(f"Could not translate codes in codelist. Error:{e}")

                        concept = data_chart["legendConcept"]
                        df = translate_df(
                            df, concept, metadata_codelist_items_translated
                        )

                    fig = draw_chart(df, data_chart)

                    text = get_static_metatada(
                        data_chart,
                        chart_id,
                        metadata_dataflow_translated,
                        df,
                        valuelist,
                    )

                    texts.append(text)
                    graphs.append(fig)

                chart = dbc.Card(
                    [
                        dbc.Row(texts, className="d-flex justify-content-around"),
                        dbc.Row(graphs, className="d-flex justify-content-around"),
                    ]
                )
                charts_per_r.append(chart)

            return charts_per_r, footer, value

        except Exception as e:
            print(e)


if __name__ == "__main__":
    app.run(debug=False, dev_tools_ui=False, dev_tools_props_check=False)
