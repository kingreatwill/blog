from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

NAME = "iblog"
VERSION = "1.0.0"
REQUIRES = ["flask>=1.1.2", "kafka-python >= 2.0.1", "pika>=1.1.0", "apscheduler>=3.6.3"]

setup(
    name=NAME,
    version=VERSION,
    # license='MIT',
    description="Issue blog.",
    author_email="",
    url="https://github.com/openjw/blog",
    keywords=["issue", "blog"],
    packages=["iblog"],
    install_requires=REQUIRES,
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
