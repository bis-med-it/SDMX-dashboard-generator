"""Module providing sdmx utilities"""
import re

import aiohttp
import pandas as pd
import requests
import sdmxthon


class SDMXData:
    """A class to get the data from SDMX API in SDMX format

    :param url_data: the API URL from which to pull the data

    """

    def __init__(self, data):
        self.url_data = data

    def get_data(self, yAxisConcept: str = None) -> pd.DataFrame:
        """Returns a Pandas DataFrame with the data requested and optionally
        set the yAxisConcept as float.

        :param yAxisConcept: str, optional: the y-axis to convert to numeric.
        :returns: pd.DataFrame: the requested data.

        """
        try:
            response = requests.get(self.url_data, timeout=30)

            if response.status_code == 200:
                try:
                    message = sdmxthon.read_sdmx(response.text)
                    resource = message.payload[list(message.payload)[0]]
                    data = resource.data
                    if yAxisConcept:
                        data[yAxisConcept] = pd.to_numeric(
                            data[yAxisConcept], errors="coerce"
                        )

                    if not isinstance(data, pd.DataFrame):
                        raise ValueError("Data is not a Pandas dataframe")

                    return data

                except Exception as e:
                    print(e)

        except ConnectionError as e:
            print(e)

        except Exception as e:
            print(e)

    async def get_data_async(self, yAxisConcept: str) -> pd.DataFrame:
        """Asynchronously returns a Pandas DataFrame with the data requested and
        optionally set the yAxisConcept as float.

        :param yAxisConcept: str, optional: the y-axis to convert to numeric.
        :returns: pd.DataFrame: the requested data.

        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url_data) as response:
                    if response.status == 200:
                        try:
                            message = sdmxthon.read_sdmx(await response.text())
                            resource = message.payload[list(message.payload)[0]]
                            data = resource.data
                            if yAxisConcept:
                                data[yAxisConcept] = pd.to_numeric(
                                    data[yAxisConcept], errors="coerce"
                                )

                            if not isinstance(data, pd.DataFrame):
                                raise ValueError("Data is not a Pandas dataframe")

                            return data

                        except Exception as e:
                            print(e)

        except ConnectionError as e:
            print(e)

        except Exception as e:
            print(e)


def _check_string(string: str, url: str):
    """Checks that the url contains the string and if not formats it appropriately

    :param string: str: the string that needs to be contained in the url
    :param url: str: the url
    :returns: str: the formatted url

    """
    try:
        if string in url:
            pass
        elif "?" in url:
            url = url + "&" + string
        else:
            url = url + "?" + string
    except Exception as e:
        print(e)

    return url


def get_components(url: str, descendants: bool = True):
    """Retrieve a dictionary with the SDMX data

    :param url: str: the API URL from which to pull the data
    :param descendants: bool: whether to include all descendants in the call to the API
                              (Default = True)
    :returns: dict: a dictionary in JSON format with the data/metadata requested.

    """

    try:
        if descendants:
            url = _check_string("references=descendants", url)

        with requests.get(url, stream=True, timeout=30) as response:
            message = sdmxthon.read_sdmx(response.text, validate=False)
            components_available = list(message.payload)
            components = {i: message.payload[i] for i in components_available}

            if components:
                return components

    except Exception as e:
        print(e)


async def get_components_async(url: str, descendants: bool = True):
    """Asynchronously retrieve a dictionary with the SDMX data

    :param url: str: the API URL from which to pull the data
    :param descendants: bool: whether to include all descendants in the call to the API
                              (Default = True)
    :returns: dict: a dictionary in JSON format with the data/metadata requested
    """

    try:
        if descendants:
            url = _check_string("references=descendants", url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                message = sdmxthon.read_sdmx(await response.text(), validate=False)
                components_available = list(message.payload)
                components = {i: message.payload[i] for i in components_available}

                if components:
                    return components

    except Exception as e:
        print(e)


class SDMXMetadata:
    """A class to get the metadata from SDMX API in SDMX format

    :param component: any object compatible with the `Component object \
                      <https://docs.sdmxthon.meaningfuldata.eu/packages/model/component.html>`_
    :param concept: a string that denotes the concept to translate

    """

    def __init__(self, components, concept: str = None):
        self.components = components
        self.concept = concept
        # Initialise to None attributes obtained with other methods
        self.cl_id_name = None
        self.cl_id_des = None
        self.cl_items = None

    def parse_message(self, component_type):
        """Parses the appropriate component and returns children artefacts.

        :param component_type: a string that can only take the following values:
                               Dataflows, Codelists, DataStructures, Concepts
        :returns: a dictionary with the children artefacts associated to
                  a component type.

        """
        valid = {"Dataflows", "Codelists", "DataStructures", "Concepts"}
        if component_type not in valid:
            raise ValueError(f"Error: component_type must be one of {valid}.")

        try:
            if component_type == "Codelists":
                content = self.components[component_type]

            else:
                component_id = list(self.components[component_type])[0]
                content = self.components[component_type][component_id]

            if content:
                return content

        except Exception as e:
            print(e)

    def dataflow_metadata(self):
        """Returns a dictionary with the name and description of the dataflow"""
        dataflow = self.parse_message(component_type="Dataflows")

        if dataflow:
            try:
                dataflow_name = dataflow.name
                dataflow_description = dataflow.description

                if not dataflow_description:
                    dataflow_description = ""

                return {"name": dataflow_name, "description": dataflow_description}

            except Exception as e:
                print(e)

    def datastructure_metadata(self):
        """Returns a dictionary with the id, dimensions, attributes and measures of the
        queried DSD


        """
        try:
            dsd = self.parse_message(component_type="DataStructures")

            if dsd:
                try:
                    try:
                        dsd_id = dsd.id
                    except Exception as e:
                        print(e)
                        dsd_id = ""

                    try:
                        dsd_dimensions = dsd.dimension_codes
                    except Exception as e:
                        print(e)
                        dsd_dimensions = ""

                    try:
                        dsd_attributes = dsd.attribute_codes
                    except Exception as e:
                        print(e)
                        dsd_attributes = ""

                    try:
                        dsd_measure = dsd.measure_code
                    except Exception as e:
                        print(e)
                        dsd_measure = ""

                    return {
                        "id": dsd_id,
                        "dim": dsd_dimensions,
                        "attr": dsd_attributes,
                        "measure": dsd_measure,
                    }

                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)

    def get_codelists(self):
        """Returns a `model.itemScheme.Codelist\
        <https://docs.sdmxthon.meaningfuldata.eu/packages/model/itemScheme.html#codelist>`_

        """
        try:
            codelists = self.parse_message(component_type="Codelists")
            return codelists

        except Exception as e:
            print(e)

    def get_codelist_name(self, *args, **kwargs):
        """Returns a string with the Agency, ID and version of of the codelist or a
        `model.itemScheme.Codelist\
        <https://docs.sdmxthon.meaningfuldata.eu/packages/model/itemScheme.html#codelist>`_
        if all descendants are included in the SDMX URL call

        """
        default = {"mode": "auto"}
        mode = {**default, **kwargs}["mode"]

        if mode == "auto":
            dsd = self.parse_message(component_type="DataStructures")

            dsd_components = list(dsd.content.keys())

            for dsd_component in dsd_components:
                try:
                    cl_name = dsd.content[dsd_component][
                        self.concept
                    ].local_representation.codelist
                except Exception as e:
                    print(e)
                    cl_name = ""
                return cl_name

    def get_cl(self):
        """Returns a Tuple with the name (str), description (str) and
        `model.itemScheme.Code\
        <https://docs.sdmxthon.meaningfuldata.eu/packages/model/item.html#code>`_

        """
        try:
            cl_id = self.get_codelist_name()

            try:
                self.cl_id_name = cl_id.name

            except Exception as e:
                print(e)
                self.cl_id_name = self.concept

            try:
                self.cl_id_des = cl_id.description
            except Exception as e:
                print(e)
                self.cl_id_des = ""

            self.cl_items = cl_id.items

            return self.cl_id_name, self.cl_id_des, self.cl_items

        except Exception as e:
            print("Error: " + str(e))


def get_url_cl(url_dsd, cl_name):
    """get_url_cl returns a string with the URL of the codelist

    :param url_dsd: the API URL of the DSD
    :param cl_name: the Agency, ID and version of the codelist (eg ESTAT:CL_AREA(1.0))
    :returns: a string with the URL to query against the API

    """

    endpoint = url_dsd.split("datastructure")[0]
    agency_id = re.sub(":", "", re.search(r"(.+?):", cl_name).group())
    resource_id = re.sub(":", "", re.search(r"(?<=\:)(.*?)(?=\()", cl_name).group())
    version = re.sub(":", "", re.search(r"(?<=\()(.*?)(?=\))", cl_name).group())
    cl_url = (
        endpoint
        + "codelist/"
        + agency_id
        + "/"
        + resource_id
        + "/"
        + version
        + "?detail=full"
    )
    return cl_url


def get_cl_item_name(items, item):
    """get_cl_item_name returns a string with code name

    :param items: a dictionary with the codes of the codelist
    :param item: a string with the code name
    :returns: the code name

    """

    cl_items = items

    if cl_items:
        try:
            cl_item = cl_items[item]
            cl_item_name = cl_item.name

            return cl_item_name

        except Exception as e:
            print(e)


def get_translation(content, locale: str = "en"):
    """get_translation returns a translated string, if any language other than\
                    is available. Only fr, es, de are currently supported\
                    but this list can be easily expanded. If no language is
                    detected, it defaults back to English

    :param content: a dictionary of dictionaries to translate
    :param locale: str: the language code (en, es, de, fr); defaults to "en".
    :returns: the string translated if any language is available

    """

    try:
        try:
            name = content["".join(locale)]["content"]

        except Exception as e:
            print(e)
            try:
                name = content["en"]["content"]
            except Exception as e:
                print(e)
                try:
                    name = content
                except Exception as e:
                    print(e)
                    name = ""
        return name

    except Exception as e:
        print(e)


def translate_df(df, concept, items_translated):
    """translate_df returns a translated Pandas DataFrame

    :param df: a Pandas DataFrame
    :param concept: a string with the column to translate
    :param items_translated: a dictionary with the codes translated
    :returns: pd.DataFrame: the translated DataFrame

    """

    if concept:
        try:
            if items_translated:
                try:
                    df[concept + "_id"] = df[concept]
                    df[concept] = df[concept].map(items_translated)
                except Exception as e:
                    print(e)
                    df[concept + "_id"] = df[concept]
        except Exception as e:
            print(e)

    return df
