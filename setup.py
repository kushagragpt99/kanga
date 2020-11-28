from codecs import open
from os import path
from setuptools import find_packages, setup

from kanga import __version__

url = 'https://github.com/papamarkou/kanga'

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kanga',
    version=__version__,
    description='MCMC diagnostics',
    long_description=long_description,
    url=url,
    download_url='{0}/archive/v{1}.tar.gz'.format(url, __version__),
    packages=find_packages(),
    license='MIT',
    author='Theodore Papamarkou',
    author_email='theodore.papamarkou@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
    keywords=['Bayesian', 'diagnostics', 'Markov chains', 'MCMC', 'Monte Carlo'],
    python_requires='>=3.6',
    install_requires=['numpy', 'scipy', 'statsmodels>=0.12.0', 'matplotlib>=3.3.3', 'seaborn>=0.11.0']
)
