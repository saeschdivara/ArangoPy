from setuptools import setup, find_packages
from arangodb import get_version

setup(
    name='ArangoPy',
    version= '0.2.3',
    packages=find_packages(),
    requires=[
        'slumber',
    ],
    url='https://github.com/saeschdivara/ArangoPy',
    license='MIT',
    author='saskyrardisaskyr',
    author_email='saeschdivara@gmail.com',
    description='Driver for ArangoDB'
)
