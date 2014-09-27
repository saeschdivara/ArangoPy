from setuptools import setup, find_packages
from arangodb import get_version

setup(
    name='ArangoPy',
    version= get_version(),
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
