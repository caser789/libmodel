from threading import Lock


class Object:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def _partition_model_new(cls, *args, **kwargs):
    return cls(*args, **kwargs)


class PartitionModel(object):
    _Model = None  # BaseModel

    _partition_models = {}
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        db_partition_id = None
        if 'db_partition_id' in kwargs:
            db_partition_id = kwargs.pop('db_partition_id')
        elif 'db_partition_key' in kwargs:
            db_partition_id = cls.Config.db_partition_func(kwargs.pop('db_partition_key'))
        partition_id = None
        if 'partition_id' in kwargs:
            partition_id = kwargs.pop('partition_id')
        elif 'partition_key' in kwargs:
            partition_id = cls.Config.partition_func(kwargs.pop('partition_key'))
        model_name = cls.__name__
        if db_partition_id is not None:
            model_name += '_%s' % db_partition_id
        if partition_id is not None:
            model_name += '_%s' % partition_id
        model_class = cls._partition_models.get(model_name)
        if model_class is not None:
            return model_class

        attrs = {}
        for key in cls.__dict__:
            attrs[key] = cls.__dict__[key]
        if 'objects' in attrs:
            attrs['objects'] = attrs['objects'].__class__()
        if db_partition_id is not None:
            if hasattr(cls, 'Config'):
                config = Object(**cls.Config.__dict__)
                if hasattr(config, 'db_for_read'):
                    config.db_for_read = config.db_for_read % db_partition_id
                if hasattr(config, 'db_for_write'):
                    config.db_for_write = config.db_for_write % db_partition_id
                if hasattr(config, 'db_for_all'):
                    config.db_for_all = config.db_for_all % db_partition_id
                attrs['Config'] = config
        meta = Object(**cls.Meta.__dict__)
        if partition_id is not None:
            meta.db_table = meta.db_table % partition_id
        attrs['Meta'] = meta
        attrs['new'] = classmethod(_partition_model_new)

        with cls._lock:
            model_class = cls._partition_models.get(model_name)
            if model_class is not None:
                return model_class
            model_class = type(model_name, tuple([cls._Model] + list(cls.__bases__[1:])), attrs)
            cls._partition_models[model_name] = model_class
        return model_class
