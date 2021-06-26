from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="beancount-nblock",
    version="0.1.0",
    description="A collection of beancount plugins",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Florian Preinstorfer",
    author_email="nblock@archlinux.us",
    url="https://github.com/nblock/beancount-nblock",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["beancount"],
    extras_require={
        "test": ["pytest", "pytest-cov", "pytest-randomly"],
    },
)
