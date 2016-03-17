import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ramlgnarok',
    version='0.1alpha',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description=(
        ''
    ),
    long_description=README,
    author=(
        'Pawel Kucmus, Lukasz Karbownik, Piotr Bajsarowicz, Artur Grochowski'
    ),
    author_email=(
        'pkucmus@gmail.com'
    ),
    install_requires=[
        'ramlfications==0.1.9',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU GPL v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
