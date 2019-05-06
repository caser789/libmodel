import json

from libenum import EnumBase


class ExtraDataState(EnumBase):
    ORIGINAL = 1
    STRING = 2
    DICT = 3


class ExtraDataModel(object):
    _extra_data_string = ''
    _extra_data_dict = {}
    _extra_data_state = ExtraDataState.ORIGINAL

    def save(self, *args, **kwargs):
        if 'extra_data' in self.__dict__:
            self.__dict__['extra_data'] = self.extra_data_string
        super(ExtraDataModel, self).save(*args, **kwargs)

    @property
    def extra_data_string(self):
        if self._extra_data_state != ExtraDataState.STRING:
            if self._extra_data_state == ExtraDataState.DICT:
                self._extra_data_string = json.dumps(self._extra_data_dict)
            elif self._extra_data_state == ExtraDataState.ORIGINAL:
                self._extra_data_string = self.__dict__['extra_data'] or ''
            else:
                self._extra_data_string = ''
        self._extra_data_state = ExtraDataState.STRING
        self._extra_data_dict = {}
        self.__dict__['extra_data'] = ''
        return self._extra_data_string

    @extra_data_string.setter
    def extra_data_string(self, value):
        if value is None:
            value = ''
        self._extra_data_state = ExtraDataState.STRING
        self._extra_data_dict = {}
        self.__dict__['extra_data'] = ''
        self._extra_data_string = value

    @property
    def extra_data_dict(self):
        if self._extra_data_state != ExtraDataState.DICT:
            if self._extra_data_state == ExtraDataState.STRING:
                self._extra_data_dict = json.loads(self._extra_data_string) or {}
            elif self._extra_data_state == ExtraDataState.ORIGINAL:
                self._extra_data_dict = json.loads(self.__dict__['extra_data']) or {}
            else:
                self._extra_data_dict = {}
        self._extra_data_state = ExtraDataState.DICT
        self._extra_data_string = ''
        self.__dict__['extra_data'] = ''
        return self._extra_data_dict

    @extra_data_dict.setter
    def extra_data_dict(self, value):
        if value is None:
            value = {}
        self._extra_data_state = ExtraDataState.DICT
        self._extra_data_string = ''
        self.__dict__['extra_data'] = ''
        self._extra_data_dict = value

    @property
    def extra_data(self):
        self.__dict__['extra_data'] = self.extra_data_string
        self._extra_data_dict = {}
        self._extra_data_string = ''
        self._extra_data_state = ExtraDataState.ORIGINAL
        return self.__dict__['extra_data']

    @extra_data.setter
    def extra_data(self, value):
        if value is None:
            value = ''
        self._extra_data_state = ExtraDataState.ORIGINAL
        self._extra_data_dict = {}
        self._extra_data_string = ''
        self.__dict__['extra_data'] = value

    class Meta:
        abstract = True
