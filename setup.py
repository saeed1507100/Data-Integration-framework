import os

from setuptools import find_packages, setup

BASE_PATH = os.getcwd()
with open("requirements.txt") as install_requires_file:
    requirements = install_requires_file.read().strip().split("\n")
    for i, requirement in enumerate(requirements):
        if "./" in requirement:
            requirements[i] = requirement.replace(".", f"file://{BASE_PATH}")

setup(
    name="data_integration_framework",
    description="Module containing the data integration functions",
    license="Apache License 2.0",
    author="SaeedKhan",
    author_email="saeedkhan.kuet.cse@gmail.com",
    keywords="airflow",
    long_description_content_type="text/markdown",
    version="1.0",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.7",
    install_requires=requirements,
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
)
