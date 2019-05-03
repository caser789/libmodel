"""
pip install mysql-python
"""
from django.conf import settings
from libmodel.django import PartitionModel
from libmodel.django import static_module


django_config = {
    'DEBUG': True,
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'test_table_partition',
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



class UserTab(PartitionModel):
    """
    create database test_table_partition character set UTF8mb4 collate utf8mb4_bin;

    use test_table_partition;
    CREATE TABLE `user_tab_00000000` (
        `transaction_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        `name` CHAR(10) NOT NULL,
        PRIMARY KEY (`transaction_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE `user_tab_00000001` (
        `transaction_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        `name` CHAR(10) NOT NULL,
        PRIMARY KEY (`transaction_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE `user_tab_00000002` (
        `transaction_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
        `name` CHAR(10) NOT NULL,
        PRIMARY KEY (`transaction_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    _Model = models.Model

    transaction_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=10, null=False)

    class Config:
        db_for_all = 'default'
        partition_func = static_module(3)

    class Meta:
        db_table = 'user_tab_%08d'
        app_label = ''


import random

name = ''.join((random.choice('abcsieuhsdfsfewoo') for _ in range(5)))

partition_key = random.choice((1, 2, 3, 4))
u = UserTab(partition_key=partition_key).new(name=name)
u.save()

m = UserTab(partition_key=partition_key).objects.filter(name=name).first()
assert m.name == name


name = ''.join((random.choice('abcsieuhsdfsfewoo') for _ in range(5)))
partition_id = 0
u = UserTab(partition_id=partition_id).new(name=name)
u.save()
m = UserTab(partition_id=partition_id).objects.filter(name=name).first()
assert m.name == name

name = ''.join((random.choice('abcsieuhsdfsfewoo') for _ in range(5)))
partition_id = 1
u = UserTab(partition_id=partition_id).new(name=name)
u.save()
m = UserTab(partition_id=partition_id).objects.filter(name=name).first()
assert m.name == name

name = ''.join((random.choice('abcsieuhsdfsfewoo') for _ in range(5)))
partition_id = 2
u = UserTab(partition_id=partition_id).new(name=name)
u.save()
m = UserTab(partition_id=partition_id).objects.filter(name=name).first()
assert m.name == name
