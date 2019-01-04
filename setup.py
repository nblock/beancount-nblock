from setuptools import setup

setup(
    name="beancount-nblock",
    version="0.0.1",
    description="A collection of beancount plugins",
    author="Florian Preinstorfer",
    author_email="nblock@archlinux.us",
    url="https://nblock.org",
    packages=["beancount_nblock"],
    install_requires=["beancount"],
    extras_require={
        "style": ["black", "flake8", "isort"],
        "test": ["pytest", "pytest-cov", "pytest-randomly", "pytest-xdist"],
    },
)
