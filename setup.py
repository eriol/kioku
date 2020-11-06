"""Setup for kioku."""
from setuptools import find_packages, setup

setup(
    name="kioku",
    version="0.1.0a",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["kioku=kioku.main:main"]},
)
