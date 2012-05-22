from setuptools import setup

version = '0.6dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('TODO.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django == 1.3.1',
    'django-staticfiles',
    'django-extensions',
    'OWSLib',
    'lizard-ui == 3.15',
    'lizard-map == 3.31',
    'lizard-maptree < 1.0.0',
    'django-nose',
    'pkginfo',
    'requests',
    ],

tests_require = [
    ]

setup(name='lizard-wms',
      version=version,
      description="App for (external) wms layers.",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=['wms'],
      author='Jack Ha',
      author_email='jack.ha@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['lizard_wms'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require = {'test': tests_require},
      entry_points={
        'console_scripts': [
            ],
        'lizard_map.adapter_class': [
            'wms = lizard_wms.layers:AdapterWMS',
            ],
        },
      )
