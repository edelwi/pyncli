import setuptools
from pyncli import __version__ as pyncli_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyncli",
    version=pyncli_version,
    author="Evgeniy Semenov",
    author_email="edelwi@yandex.ru",
    description="Command Line Interface for NextCloud GroupFolder app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edelwi/pyncli",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts':
            ['pnc = pyncli.nc:main',
             'pnc_test =  pyncli.test.runall:main',
            ]
        },
    install_requires=[
        'ldap3>=2.5.1',
        'requests>=2.18.4',
        'lxml>=4.2.5',
        'python-dotenv>=0.10.0'
        'certifi'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)