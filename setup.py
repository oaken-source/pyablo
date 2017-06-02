
from os.path import join, dirname
from setuptools import setup


setup(
    name='pyablo',
    version='0.1',
    maintainer='Andreas Grapentin',
    maintainer_email='andreas@grapentin.org',
    url='https://github.com/oaken-source/pyablo',
    description='A(nother) free implementation of the Diablo game engine',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),

    keywords='diablo game',
    packages=['pyablo'],

    entry_points={
        'console_scripts': [
            'pyablo = pyablo.__main__:main',
        ],
    },

    install_requires=[
        'av',
        'mpq',
        'numpy',
        'pygame',
    ],

    license='GPLv3',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment',
    ],

    test_suite='tests',
    tests_require=[
        'pytest',
    ],

    setup_requires=['pytest_runner'],
)
