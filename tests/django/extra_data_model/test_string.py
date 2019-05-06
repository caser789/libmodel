import json
import unittest

from libmodel.django.extra_data_model import ExtraDataModel
from libmodel.django.extra_data_model import ExtraDataState


class StringTestCase(unittest.TestCase):

    def test_get_extra_data_string_from_string_state(self):
        m = ExtraDataModel()
        m._extra_data_state = ExtraDataState.STRING
        edd = m._extra_data_dict = {'a': 1}
        ed = m.__dict__['extra_data'] = 'abc'
        eds = m._extra_data_string = 'ddd'

        self.assertEqual(m.extra_data_string, eds)
        self.assertEqual(m._extra_data_state, ExtraDataState.STRING)
        self.assertEqual(m._extra_data_dict, {})
        self.assertEqual(m.__dict__['extra_data'], '')

    def test_get_extra_data_string_from_origin_state(self):
        m = ExtraDataModel()
        m._extra_data_state = ExtraDataState.ORIGINAL
        edd = m._extra_data_dict = {'a': 1}
        ed = m.__dict__['extra_data'] = 'abc'
        eds = m._extra_data_string = 'ddd'

        self.assertEqual(m.extra_data_string, ed)
        self.assertEqual(m._extra_data_state, ExtraDataState.STRING)
        self.assertEqual(m._extra_data_dict, {})
        self.assertEqual(m.__dict__['extra_data'], '')

    def test_get_extra_data_string_from_dict_state(self):
        m = ExtraDataModel()
        m._extra_data_state = ExtraDataState.DICT
        edd = m._extra_data_dict = {'a': 1}
        ed = m.__dict__['extra_data'] = 'abc'
        eds = m._extra_data_string = 'ddd'

        self.assertEqual(m.extra_data_string, json.dumps(edd))
        self.assertEqual(m._extra_data_state, ExtraDataState.STRING)
        self.assertEqual(m._extra_data_dict, {})
        self.assertEqual(m.__dict__['extra_data'], '')

    def test_set_extra_data_string(self):
        m = ExtraDataModel()
        m._extra_data_state = ExtraDataState.DICT
        edd = m._extra_data_dict = {'a': 1}
        ed = m.__dict__['extra_data'] = 'abc'
        eds = m._extra_data_string = 'ddd'

        value = 'fff'
        m.extra_data_string = value

        self.assertEqual(m._extra_data_state, ExtraDataState.STRING)
        self.assertEqual(m._extra_data_dict, {})
        self.assertEqual(m.__dict__['extra_data'], '')
        self.assertEqual(m._extra_data_string, value)


if __name__ == '__main__':
    unittest.main()
