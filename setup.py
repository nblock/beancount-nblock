from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="beancount-nblock",
    version="0.0.2",
    description="A collection of beancount plugins",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Florian Preinstorfer",
    author_email="nblock@archlinux.us",
    url="https://github.com/nblock/beancount-nblock",
    packages=["beancount_nblock"],
    install_requires=["beancount"],
    extras_require={
        "style": ["black", "flake8", "isort"],
        "test": ["pytest", "pytest-cov", "pytest-randomly", "pytest-xdist"],
    },
)
