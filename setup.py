from distutils.core import setup
import setuptools

setup(
    name='organize',
    version='0.1.1',
    author='Will Larson',
    author_email='lethain@gmail.com',
    packages=['organize', 'organize.tests'],
    url='http://pypi.python.org/pypi/organize/',
    license='LICENSE.txt',
    description='Parse real-world tabular data in a wide variety of formats.',
    long_description=open('README.md').read(),
    install_requires=['xlrd'],
)
