from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Devops-DB'
LONG_DESCRIPTION = 'Module with general-purpose DevOps-DB functions.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="devopsdb",
        version=VERSION,
        author="Fausto Branco",
        author_email="fausto.branco@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
)