import json
import unittest

from libmodel.django.extra_data_model import ExtraDataModel
from libmodel.django.extra_data_model import ExtraDataState


class DictTestCase(unittest.TestCase):

    def test_get_extra_data_dict_from_dict_state(self):
        m = ExtraDataModel()
        m._extra_data_state = ExtraDataState.DICT
        edd = m._extra_data_dict = {'a': 1}
        ed = m.__dict__['extra_data'] = 'abc'
        eds = m._extra_data_string = 'ddd'

        self.assertEqual(m.extra_data_dict, edd)
        self.assertEqual(m._extra_data_state, ExtraDataState.DICT)
        self.assertEqual(m._extra_data_string, '')
        self.assertEqual(m.__dict__['extra_data'], '')

    def test_get_extra_data_dict_from_origin_state(self):
        m = ExtraDataModel()
        m._extra_data_state = ExtraDataState.ORIGINAL
        edd = m._extra_data_dict = {'a': 1}
        ed = m.__dict__['extra_data'] = json.dumps({'b': 2})
        eds = m._extra_data_string = 'ddd'

        self.assertEqual(m.extra_data_dict, {'b': 2})
        self.assertEqual(m._extra_data_state, ExtraDataState.DICT)
        self.assertEqual(m._extra_data_string, '')
        self.assertEqual(m.__dict__['extra_data'], '')

    def test_get_extra_data_dict_from_string_state(self):
        m = ExtraDataModel()
        m._extra_data_state = ExtraDataState.STRING
        edd = m._extra_data_dict = {'a': 1}
        ed = m.__dict__['extra_data'] = 'abc'
        eds = m._extra_data_string = json.dumps({'b': 2})

        self.assertEqual(m.extra_data_dict, {'b': 2})
        self.assertEqual(m._extra_data_state, ExtraDataState.DICT)
        self.assertEqual(m._extra_data_string, '')
        self.assertEqual(m.__dict__['extra_data'], '')

    def test_set_extra_data_dict(self):
        m = ExtraDataModel()
        m._extra_data_state = ExtraDataState.STRING
        edd = m._extra_data_dict = {'a': 1}
        ed = m.__dict__['extra_data'] = 'abc'
        eds = m._extra_data_string = 'ddd'

        value = {'b': 2}
        m.extra_data_dict = value

        self.assertEqual(m._extra_data_state, ExtraDataState.DICT)
        self.assertEqual(m._extra_data_string, '')
        self.assertEqual(m.__dict__['extra_data'], '')
        self.assertEqual(m._extra_data_dict, value)


if __name__ == '__main__':
    unittest.main()
