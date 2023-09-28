"""Module providing generic utilities"""
import re

CLEANR = re.compile("<.*?>")


def cleanhtml(raw_html):
    """Clean raw html

    :param raw_html: str: the input to clean
    :returns: str: the cleaned text

    """
    cleantext = re.sub(CLEANR, "", raw_html)
    return cleantext
