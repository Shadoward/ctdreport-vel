# -*- coding: utf-8 -*-
# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_namespace_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

install_requires = [
    'argparse',
    'numpy',
    'pandas',
    'glob',
    'tqdm',
    'bokeh',
]

extras_require = {
    'build' : [
        'setuptools',
    ],
    'tests' : [],
}

setup(
    name='ctdreportvel',
    version='0.1.1',
    description='CTD Interactif Report for Starfix .vel files.',
    long_description=readme,
    author='Patrice Ponchant',
    author_email='patrice.ponchant@furgo.com',
    include_package_data = True,
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=extras_require['tests'],
    url='',
    license=license,
    packages=find_namespace_packages(where='src'),
    package_dir={'': 'src'},
    keywords='CTD vel Bokeh HTML',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering'
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

