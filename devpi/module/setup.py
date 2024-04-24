from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Convert IP to Int'
LONG_DESCRIPTION = 'Module to convert IPs into Numbers and Numbers into IPs.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="ip_number", 
        version=VERSION,
        author="Fausto Branco",
        author_email="fausto.branco@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
)