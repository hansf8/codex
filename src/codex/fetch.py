"""
"""

import configparser
import io
import os

import pandas as pd

import requests
from requests.exceptions import RequestException


CONFIG_PATH = os.path.expanduser('~/config.ini')
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_PATH)
KEY = CONFIG['enigma']['key']

ENIGMA_BASE_URL = 'https://public.enigma.com/api/'
ENIGMA_HEADERS = {'authorization': 'Bearer {}'.format(KEY)}


# ------------------------------------------------------------------------------
# Enigma
# ------------------------------------------------------------------------------


def enigma_export(dataset_id, headers=ENIGMA_HEADERS, **kwargs):
    """Export an Enigma dataset into a pandas dataframe.

    Parameters
    ----------
    kwargs
        Keyword arguments for pands read csv function.

    Returns
    -------
    pandas.DataFrame
    """
    snapshot_id = enigma_snapshot_id(dataset_id, headers=headers)
    print('Retrieved snapshot ID...')
    url = ENIGMA_BASE_URL + 'export/{}'.format(snapshot_id)
    print('Making request to API...')
    response = make_request(url, headers=headers)
    print('Response received...')
    decoded_content = response.content.decode('utf-8')
    data = io.StringIO(decoded_content)
    export = pd.read_csv(data, **kwargs)
    print('Finished export.')
    return export


def enigma_snapshot_id(dataset_id, headers=ENIGMA_HEADERS):
    """Return the snapshot ID of an enigma dataset. Typically used in retrieving
    an export.

    Returns
    -------
    snapshot_id : str

    Examples
    --------
    enigma_snapshot_id('fa7ab996-fb43-4e86-80e7-f8e82ccba15f')
    >>>
    """
    # We're only interested in the dataset's metadata, so limit rows to 1.
    json = enigma_dataset(dataset_id, headers=headers, row_limit=1)
    return json['current_snapshot']['id']


def enigma_dataset(dataset_id, headers=ENIGMA_HEADERS, row_limit=100):
    """Return an enigma dataset in json form.

    Parameters
    ----------
    row_limit : int
        Number of rows of the dataset to return. Default is 100.

    Returns
    -------
    json : dict
    """
    row_limit_query = '?&row_limit={}'.format(row_limit)
    url = ENIGMA_BASE_URL + 'datasets/{}'.format(dataset_id) + row_limit_query
    response = requests.get(url, headers=headers)
    return response.json()


def make_request(url, **kwargs):
    """Make a request and return the response."""
    try:
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        return response
    except RequestException as error:
        print(error)
