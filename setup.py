from distutils.core import setup

setup(
    name='organize',
    version='0.1.0',
    author='Will Larson',
    author_email='lethain@gmail.com',
    packages=['organize', 'organize.tests', 'organize.examples'],
    url='http://pypi.python.org/pypi/organize/',
    license='LICENSE.txt',
    description='Parse real-world tabular data in a wide variety of formats.',
    long_description=open('README.md').read(),
)
