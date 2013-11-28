from setuptools import setup, find_packages

__version_info__ = ('0', '0', '5')
__version__ = '.'.join(__version_info__)

setup(
    name="twosheds",
    version=__version__,
    description="extensible shell implemented in Python",
    author="Ceasar Bautista",
    author_email="cbautista2010@gmail.com",
    url="https://github.com/Ceasar/twosheds",
    keywords=["twosheds", "shell"],
    packages=["twosheds"],
    scripts=["scripts/twosheds"],
    classifiers=[
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    ],
    use_2to3=True,
)
