import os

from setuptools import find_packages, setup

def get_version():
    init_py_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "py3d", "__init__.py"
    )
    init_py = open(init_py_path, "r").readlines()
    version_line = [l.strip() for l in init_py if l.startswith("__version__")][0]
    version = version_line.split("=")[-1].strip().strip("'\"")
    return version


setup(
    name="py3d",
    version=get_version(),
    url="https://github.com/fluentgcc/py3d.git",
    license="Apache 2.0",
    author="fluentgcc",
    description="Collection of useful python 3d tools",
    python_requires=">=3.6",
    install_requires=[
        "numpy",
    ],
    packages=find_packages(exclude=("tests",)),
)
