"""
This module contains helper functions for use in testing.

The BaseCase class forms the main functionality of this module.
"""

import os


filer_dir = os.path.dirname(__file__)
FIXTURES_DIR = os.path.join(filer_dir, 'fixtures/')


class BaseCase(object):
    """Helper framework for testing a class or function.

    A data dictionary is used to generate an instance of the class to be tested
    (i.e., the test class). Key attributes of the test class are then extracted
    and saved as instance attributes.

    Use of this class in conjunction with pytest's fixtures feature greatly
    simplifies tests:

        data = [{
            '_baz': 'qux',  # Input for func_to_test
            'foo': 'bar'        # Expected output from func
        }]

        class ExampleCase(BaseCase):
            def gen_testable_attributes(self):
                # _baz has automatically been loaded as an attribute by the
                # _load_data method.
                self.foo_ = func_to_test(self._baz)

        @pytest.fixture(scope='module', params=data)
        def example_case(request):
            return ExampleCase(request.param)

        def test_example(example_case):
            assert example_case.foo_ == excample.case.foo

    This framework makes it very asy to add extra attributes to test or
    additional fixtures.

    Parameters
    ----------
    data : dict
        Includes data necessary to generate an instance of the test class
        (indicated with a leading underscore) and the correct values for
        testable attributes of the test class.

    Attributes
    ----------
    Correct values for testable attributes of test class (see Parameters).

    Testable attributes of instance. Keys for these attributes have a trailing
    underscore.

    Methods
    -------
    additional_data_loading
        Allows for specifying additional data loading logic.
    """

    def __init__(self, data):
        self._load_data(data)
        self.gen_test_class_instance()
        self.gen_testable_attributes()

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def _load_data(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        self.additional_data_loading()

    def additional_data_loading(self):
        pass

    def gen_test_class_instance(self):
        """Generate an instance of the test class as well as any required
        intermediate values.
        """
        pass

    def gen_testable_attributes(self):
        """Extract the test class attributes that need to be tested and save
        them as attributes of self.
        """
        pass

    def save_testable_attributes(self, dct, keys):
        """Given a list of keys and a dictionary, save the corresponding
        dictionary items to self using the same keys (with an additional
        leading underscore) as attribute names.

        Useful for bulk saving testable attributes from a test class to the
        instance.

        Parameters
        ----------
        dct : dict

        keys : list of str

        Examples
        --------
        >>> case = BaseCase()
        >>> dct = {'foo': 'bar', 'baz': 'qux'}
        >>> case.save_testable_attributes(dct, ['foo', 'baz'])
        >>> case.foo_
        'bar'
        >>> case.baz_
        'qux'
        """
        for key in keys:
            setattr(self, key + '_', dct[key])
