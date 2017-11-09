from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyzwave',
    version='1.0.1',
    description='A Z-Wave interfacing library in python',
    long_description=long_description,
    url='https://github.com/ebisso/pyzwave',
    author='Eric Bissonnette',
    author_email='ebisso.dev@gmail.com',
    license='MIT',
    packages=['pyzwave'],
    install_requires=['pyserial'],
)