from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str) -> List[str]:
    '''
    This function returns a list of project requirements
    '''

    requirements = []

    with open(file_path, 'r') as file:
        requirements = file.readlines()
        requirements = [ requirement.replace('\n', '') for requirement in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


# Configures the setup
setup(
    name='db_project',
    version='0.0.1',
    author='Alexander Burgos',
    author_email='a.burgos.n05@gmail.com',
    packages=find_packages(), # Looks for all folders with __init__.py file
    install_requires=get_requirements('requirements.txt')
)