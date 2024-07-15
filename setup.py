from setuptools import setup, find_packages

setup(
    name='schwab_api',
    version='0.1.0',
    description='A Python package for interacting with the Charles Schwab API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Emi Harry',
    author_email='pypackages@nainatechcorp.com',
    url='https://github.com/ENHarry/schwab_api',
    packages=find_packages(),
    install_requires=[
        'requests',
        'json'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
