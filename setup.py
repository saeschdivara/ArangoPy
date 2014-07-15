from setuptools import setup

setup(
    name='ArangoPy',
    version='0.0.9',
    packages=['arangodb'],
    requires=[
        'slumber',
    ],
    url='https://github.com/saeschdivara/ArangoPy',
    license='MIT',
    author='saskyrardisaskyr',
    author_email='saeschdivara@gmail.com',
    description='Driver for ArangoDB'
)
