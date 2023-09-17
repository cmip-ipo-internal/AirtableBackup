# setup.py

from setuptools import setup

setup(
    name='airtable_backup',
    version='0.1',
    description='A script to backup the entire workspace in Airtable',
    author='Daniel Ellis (@wolfiex)',
    author_email='daniel.ellis (at) ext.esa.int',
    packages=['airtable_backup'],
    install_requires=[
        'requests',
        'tqdm',
        'pandas',
    ],
)

