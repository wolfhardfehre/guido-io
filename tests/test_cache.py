import pickle
import shutil
import unittest
from unittest.mock import patch

from app.commons.cache import cache
from tests import TEST_TMP_PATH


@cache(folder=TEST_TMP_PATH, use_cache=True)
def function():
    return 'some_thing'


class TestCache(unittest.TestCase):

    def tearDown(self) -> None:
        shutil.rmtree(TEST_TMP_PATH)

    @patch.object(pickle, 'load')
    def test_function(self, mock_pickle_load):
        function()
        function()
        first_file = next(TEST_TMP_PATH.glob('*'))
        self.assertRegex(first_file.name, r'^Function.function.pkl')
        mock_pickle_load.assert_called_once()

    @patch.object(pickle, 'load')
    def test_instance_method(self, mock_pickle_load):
        self.instance_method(self.series, param2=0)
        self.instance_method(self.series, param2=0)
        first_file = next(TEST_TMP_PATH.glob('*'))
        self.assertRegex(first_file.name, r'^TestCache.instance_method_[\w]{32}_[\w]{32}.pkl')
        mock_pickle_load.assert_called_once()

    @patch.object(pickle, 'load')
    def test_instance_method_no_cache_load_with_different_series(self, mock_pickle_load):
        self.instance_method(dict(a=1), param2=0)
        self.instance_method(dict(a=0), param2=0)
        first_file = next(TEST_TMP_PATH.glob('*'))
        self.assertRegex(first_file.name, r'^TestCache.instance_method_[\w]{32}_[\w]{32}.pkl')
        mock_pickle_load.assert_not_called()

    @patch.object(pickle, 'load')
    def test_static_method(self, mock_pickle_load):
        self.static_method(2, param2=self.frame)
        self.static_method(2, param2=self.frame)
        first_file = next(TEST_TMP_PATH.glob('*'))
        self.assertRegex(first_file.name,  r'^Function.static_method_[\w]{32}_[\w]{32}.pkl')
        mock_pickle_load.assert_called_once()

    @patch.object(pickle, 'load')
    def test_static_method_no_params(self, mock_pickle_load):
        self.static_method_no_params()
        self.static_method_no_params()
        first_file = next(TEST_TMP_PATH.glob('*'))
        self.assertRegex(first_file.name,  r'^Function.static_method_no_params.pkl')
        mock_pickle_load.assert_called_once()

    @patch.object(pickle, 'load')
    def test_static_method_only_kwargs(self, mock_pickle_load):
        self.static_method(param1=2, param2=self.frame)
        self.static_method(param1=2, param2=self.frame)
        first_file = next(TEST_TMP_PATH.glob('*'))
        self.assertRegex(first_file.name,  r'^Function.static_method_[\w]{32}.pkl')
        mock_pickle_load.assert_called_once()

    @patch.object(pickle, 'load')
    def test_class_method(self, mock_pickle_load):
        self.class_method(2, param2=self.frame)
        self.class_method(2, param2=self.frame)
        first_file = next(TEST_TMP_PATH.glob('*'))
        self.assertRegex(first_file.name,  r'^TestCache.class_method_[\w]{32}_[\w]{32}.pkl')
        mock_pickle_load.assert_called_once()

    @patch.object(pickle, 'load')
    def test_sub_folder(self, mock_pickle_load):
        self.with_sub_folder(2, param2=self.frame)
        self.with_sub_folder(2, param2=self.frame)
        first_file = next(TEST_TMP_PATH.glob('sub/*'))
        self.assertRegex(first_file.name, r'^TestCache.with_sub_folder_[\w]{32}_[\w]{32}.pkl')
        self.assertTrue((TEST_TMP_PATH / 'sub').exists())
        mock_pickle_load.assert_called_once()

    @cache(folder=TEST_TMP_PATH, use_cache=True)
    def instance_method(self, param1, param2):      # pylint: disable=no-self-use
        return f'{param1}, {param2}'

    @staticmethod
    @cache(folder=TEST_TMP_PATH, use_cache=True)
    def static_method(param1, param2):
        return f'{param1}, {param2}'

    @staticmethod
    @cache(folder=TEST_TMP_PATH, use_cache=True)
    def static_method_no_params():
        return 'something'

    @classmethod
    @cache(folder=TEST_TMP_PATH, use_cache=True)
    def class_method(cls, param1, param2):
        return f'{param1}, {param2}'

    @cache(folder=TEST_TMP_PATH, sub_folder='sub', use_cache=True)
    def with_sub_folder(self, param1, param2):      # pylint: disable=no-self-use
        return f'{param1}, {param2}'

    @property
    def frame(self) -> dict:
        return {'a': [1, 2], 'b': [3, 4]}

    @property
    def series(self) -> dict:
        return {'a': 1, 'b': 3}
