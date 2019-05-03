"""
pip install mysql-python
"""
from django.conf import settings


django_config = {
    'DEBUG': True,
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'test_db',
            'USER': 'root',
            'PASSWORD': 'mysql',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'CONN_MAX_AGE': 3600,
            'OPTIONS': {'charset': 'utf8mb4'},
        },
    },
}
settings.configure(**django_config)


from django.db import models

from libmodel.django import PartitionModel


class UserTab(PartitionModel):
    """
    create database test_db character set UTF8mb4 collate utf8mb4_bin;

    CREATE TABLE `user_tab` (
        `transaction_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        `name` CHAR(10) NOT NULL,
        PRIMARY KEY (`transaction_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    _Model = models.Model

    transaction_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=10, null=False)

    class Config:
        db_for_all = 'test_dbc'

    class Meta:
        db_table = 'user_tab'
        app_label = ''


import random

name = ''.join((random.choice('abcsieuhsdfsfewoo') for _ in range(5)))

u = UserTab().new(name=name)
u.save()

m = UserTab().objects.filter(name=name).first()
assert m.name == name
