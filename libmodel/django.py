from threading import Lock


class Object:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def _new(cls, *args, **kwargs):
    return cls(*args, **kwargs)


class PartitionModel(object):
    """PartitionModel support db partition, table partion or both

    Usage:

    class UserTab(db.PartitionModel):
        id = db.BigAutoField(primary_key=True)
        uid = db.PositiveBigIntegerField()
        login_time = db.PositiveIntegerField()

        class Config:
            db_for_all = 'log_db_%s'

            @staticmethod
            def static_lower(s):
                return s.lower()

            partition_func = db.partition_by_datetime('%Y%m%d')
            db_partition_func = lambda : 1  # generate db_partition_id with db_partition_key

        class Meta:
            app_label = ''
            db_table = u'user_login_log_tab_%s'

    UserTab(db_partition_key='SG', partition_key=time.time()).objects.filter(uid=10000)
    UserTab(db_partition_id='sg', partition_id='20160101')(uid=10000, login_time=time.time()).save()


    :param db_partition_id:
    :param db_partition_key:
    :param partition_id:
    :param partition_key:
    """

    _model_class_store = {}
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        # get db_partion_id from kw or generate by db_partition_key with db_partition_func
        db_partition_id = None
        if 'db_partition_id' in kwargs:
            db_partition_id = kwargs.pop('db_partition_id')
        elif 'db_partition_key' in kwargs:
            db_partition_id = cls.Config.db_partition_func(kwargs.pop('db_partition_key'))

        # get partion_id from kw or generate by partition_key with partition_func
        partition_id = None
        if 'partition_id' in kwargs:
            partition_id = kwargs.pop('partition_id')
        elif 'partition_key' in kwargs:
            partition_id = cls.Config.partition_func(kwargs.pop('partition_key'))

        # model name
        model_name = cls.__name__
        if db_partition_id is not None:
            model_name += '_%s' % db_partition_id
        if partition_id is not None:
            model_name += '_%s' % partition_id
        model = cls._model_class_store.get(model_name)
        if model is not None:
            return model

        attrs = {}
        for key, value in cls.__dict__.items():
            attrs[key] = value
        if 'objects' in attrs:
            attrs['objects'] = attrs['objects'].__class__()

        if db_partition_id is not None:
            config = Object(cls.Config.__dict__)
            if hasattr(config, 'db_for_read'):
                config.db_for_read = config.db_for_read % db_partition_id
            if hasattr(config, 'db_for_write'):
                config.db_for_write = config.db_for_write % db_partition_id
            if hasattr(config, 'db_for_all'):
                config.db_for_all = config.db_for_all % db_partition_id
            attrs['Config'] = config

        meta = Object(cls.Meta.__dict__)
        if partition_id is not None:
            meta.db_table = meta.db_table % partition_id
        attrs['Meta'] = meta
        attrs['new'] = classmethod(_new)

        with cls._lock:
            model_class = cls._model_class_store.get(model_name)
            if model_class is not None:
                return model_class
            model_class = type(
                model_name,
                tuple(),
                attrs
            )
            cls._model_class_store[model_name] = model_class
        return model_class
