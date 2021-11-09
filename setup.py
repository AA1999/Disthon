from setuptools import setup

with open("README.md", "r") as file:
    long_des = file.read()

setup(
    name="disthon",
    packages=[],
    install_requires=["aiohttp", "yarl", "pydantic", "arrow"],
    description="An API wrapper for the discord API written in python",
    version="0.0.1",
    long_description=long_des,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Arshia",
    author_email="arshia.aghaei@gmail.com",
    url="https://github.com/AA1999/Disthon",
    keywords=["API", "discord"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
    ]
)
