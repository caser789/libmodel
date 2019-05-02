"""
libmodel
-------------------
libmodel provide model libs
"""
from setuptools import setup

setup(name='libmodel',
      version='0.0.1',
      url='https://github.com/caser789/libmodel',
      license='MIT',
      author='Xue Jiao',
      author_email='jiao.xuejiao@gmail.com',
      description='model libs',
      long_description='model libs',
      keywords = ['model', 'lib', 'django', 'flask'],
      packages=['libmodel'],
      zip_safe=False,
      platforms='any',
      install_requires=[],
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ])
