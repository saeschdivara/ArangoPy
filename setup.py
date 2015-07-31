from setuptools import setup, find_packages

setup(
    name='ArangoPy',
    version= '0.5.7',
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
