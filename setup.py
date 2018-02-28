import re
from setuptools import setup


with open('README.rst', 'r') as f:
    readme = f.read()

with open('cpms/__init__.py', 'r') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name="Cpms",
    version=version,
    packages=['cpms'],
    author='Rizha Musthafa',
    author_email='rizha.musthafa@acommerce.asia',
    maintainer='ID Integration Team',
    maintainer_email='id.channeldev@acommerce.asia',
    description='Connector to cpms public api',
    long_description=readme,
    license='aCommerce',
    platform='any',
    install_requires=[
        'requests',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    zip_safe=False
)
