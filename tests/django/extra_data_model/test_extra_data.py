import json
import unittest

from libmodel.django.extra_data_model import ExtraDataModel
from libmodel.django.extra_data_model import ExtraDataState


class ExtraDataTestCase(unittest.TestCase):

    def test_get(self):
        m = ExtraDataModel()
        m._extra_data_state = ExtraDataState.STRING
        edd = m._extra_data_dict = {'a': 1}
        ed = m.__dict__['extra_data'] = 'abc'
        eds = m._extra_data_string = 'ddd'

        self.assertEqual(m.extra_data, eds)
        self.assertEqual(m._extra_data_state, ExtraDataState.ORIGINAL)
        self.assertEqual(m._extra_data_dict, {})
        self.assertEqual(m._extra_data_string, '')

    def test_set_extra_data_string(self):
        m = ExtraDataModel()
        m._extra_data_state = ExtraDataState.DICT
        edd = m._extra_data_dict = {'a': 1}
        ed = m.__dict__['extra_data'] = 'abc'
        eds = m._extra_data_string = 'ddd'

        value = 'fff'
        m.extra_data = value

        self.assertEqual(m._extra_data_state, ExtraDataState.ORIGINAL)
        self.assertEqual(m._extra_data_dict, {})
        self.assertEqual(m.__dict__['extra_data'], value)
        self.assertEqual(m._extra_data_string, '')


if __name__ == '__main__':
    unittest.main()
