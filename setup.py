from setuptools import setup, find_packages

setup(
    name="llm-connector",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "homeassistant>=2023.0.0",
        "aiohttp>=3.8.0",
        "voluptuous>=0.13.0",
    ],
)
