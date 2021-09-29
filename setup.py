from setuptools import setup

with open("README.md", "r") as file:
    long_des = file.read()

setup(
    name="disthon",
    packages=["discord",],
    install_requires=["aiohttp", "yarl"],
    description="An API wrapper for the discord API written in python",
    version="x.x.x",
    long_description=long_des,
    long_description_content_type="text/markdown",
    license="GPL-3.0",
    author="Arshia",
    author_email="xxx",
    url="https://github.com/AA1999/Disthon",
    keywords=["API", "discord"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ]
)
