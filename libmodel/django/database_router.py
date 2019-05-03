class DatabaseRouter(object):

    def db_for_read(self, model, **hints):
        if hasattr(model, 'Config'):
            if hasattr(model.Config, 'db_for_read'):
                return model.Config.db_for_read
            elif hasattr(model.Config, 'db_for_all'):
                return model.Config.db_for_all
        return 'default'

    def db_for_write(self, model, **hints):
        if hasattr(model, 'Config'):
            if hasattr(model.Config, 'db_for_write'):
                return model.Config.db_for_write
            elif hasattr(model.Config, 'db_for_all'):
                return model.Config.db_for_all
        return 'default'
