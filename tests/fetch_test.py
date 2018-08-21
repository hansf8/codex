"""
Tests for fetch module.
"""

import pandas as pd
import pytest

from codex.fetch import enigma_dataset, enigma_export
from tests.prep import BaseCase


ENIGMA_DATA = [
    {
        '_dataset_id': 'fa7ab996-fb43-4e86-80e7-f8e82ccba15f',
        'display_name': 'New York City, New York - Restaurant Inspections'}

]


class EnigmaCase(BaseCase):

    def gen_test_class_instance(self):
        self.dataset_ = enigma_dataset(self._dataset_id)
        self.export_ = enigma_export(self._dataset_id)

    def gen_testable_attributes(self):
        self.display_name_ = self.dataset_['display_name']


@pytest.fixture(scope='module', params=ENIGMA_DATA)
def enigma(request):
    return EnigmaCase(request.param)


def test_display_name_correct(enigma):
    assert enigma.display_name_ == enigma.display_name


def test_dataset_is_type_dict(enigma):
    assert isinstance(enigma.dataset_, dict)


def test_export_is_type_dataframe(enigma):
    assert isinstance(enigma.export_, pd.DataFrame)
