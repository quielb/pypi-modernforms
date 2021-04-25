import pathlib
import setuptools
from setuptools import setup
import modernforms

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="modernforms",
    version=modernforms.__version__,
    description="An interface to control ModerForms smart fans",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/quielb/pypi-modernforms",
    author="Barry Quiel",
    author_email="barry.quiel@gmail.com",
    license="GPL",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=False,
    install_requires=["requests"],
)
