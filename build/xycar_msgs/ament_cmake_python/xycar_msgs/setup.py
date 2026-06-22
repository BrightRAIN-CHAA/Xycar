from setuptools import find_packages
from setuptools import setup

setup(
    name='xycar_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('xycar_msgs', 'xycar_msgs.*')),
)
