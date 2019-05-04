Database Partition
==============

need to `pip install mysql-python`

need to `pip install django`

.. code-block:: python
  from django.conf import settings

  from libmodel.django import static_module
  from libmodel.django import PartitionModel

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
          'test_db_00000000': {
              'ENGINE': 'django.db.backends.mysql',
              'NAME': 'test_db_00000000',
              'USER': 'root',
              'PASSWORD': 'mysql',
              'HOST': '127.0.0.1',
              'PORT': '3306',
              'CONN_MAX_AGE': 3600,
              'OPTIONS': {'charset': 'utf8mb4'},
          },
          'test_db_00000001': {
              'ENGINE': 'django.db.backends.mysql',
              'NAME': 'test_db_00000001',
              'USER': 'root',
              'PASSWORD': 'mysql',
              'HOST': '127.0.0.1',
              'PORT': '3306',
              'CONN_MAX_AGE': 3600,
              'OPTIONS': {'charset': 'utf8mb4'},
          },
          'test_db_00000002': {
              'ENGINE': 'django.db.backends.mysql',
              'NAME': 'test_db_00000002',
              'USER': 'root',
              'PASSWORD': 'mysql',
              'HOST': '127.0.0.1',
              'PORT': '3306',
              'CONN_MAX_AGE': 3600,
              'OPTIONS': {'charset': 'utf8mb4'},
          },
      },
      'DATABASE_ROUTERS': ['libmodel.django.DatabaseRouter']
  }
  settings.configure(**django_config)


  from django.db import models


  class UserTab(PartitionModel):
      """
      create database test_db_00000000 character set UTF8mb4 collate utf8mb4_bin;
      create database test_db_00000001 character set UTF8mb4 collate utf8mb4_bin;
      create database test_db_00000002 character set UTF8mb4 collate utf8mb4_bin;

      use test_db_00000000;
      CREATE TABLE `user_tab` (
          `transaction_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
          `name` CHAR(10) NOT NULL,
          PRIMARY KEY (`transaction_id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

      use test_db_00000001;
      CREATE TABLE `user_tab` (
          `transaction_id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
          `name` CHAR(10) NOT NULL,
          PRIMARY KEY (`transaction_id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

      use test_db_00000002;
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
          db_for_all = 'test_db_%08d'
          db_partition_func = static_module(3)

      class Meta:
          db_table = 'user_tab'
          app_label = ''


  import random

  name = ''.join((random.choice('abcsieuhsdfsfewoo') for _ in range(5)))

  db_partition_key = random.choice((1, 2, 3, 4))

  u = UserTab(db_partition_key=db_partition_key).new(name=name)
  u.save()

  m = UserTab(db_partition_key=db_partition_key).objects.filter(name=name).first()
  assert m.name == name


  name = ''.join((random.choice('abcsieuhsdfsfewoo') for _ in range(5)))
  db_partition_id = 0
  u = UserTab(db_partition_id=db_partition_id).new(name=name)
  u.save()
  m = UserTab(db_partition_id=db_partition_id).objects.filter(name=name).first()
  assert m.name == name

  name = ''.join((random.choice('abcsieuhsdfsfewoo') for _ in range(5)))
  db_partition_id = 1
  u = UserTab(db_partition_id=db_partition_id).new(name=name)
  u.save()
  m = UserTab(db_partition_id=db_partition_id).objects.filter(name=name).first()
  assert m.name == name

  name = ''.join((random.choice('abcsieuhsdfsfewoo') for _ in range(5)))
  db_partition_id = 2
  u = UserTab(db_partition_id=db_partition_id).new(name=name)
  u.save()
  m = UserTab(db_partition_id=db_partition_id).objects.filter(name=name).first()
  assert m.name == name
