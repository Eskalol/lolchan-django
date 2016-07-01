import json
import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'lolchan', 'version.json')) as f:
    version = json.loads(f.read())


setup(
    name='lolchan',
    description='The lolchan django project.',
    version='1.0',
    author='lolchan',
    packages=find_packages(exclude=['manage', 'tasks']),
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)
