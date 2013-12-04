from setuptools import setup, find_packages

import twosheds

setup(
    name="twosheds",
    version=twosheds.__version__,
    description="extensible Python shell",
    # long_desription=(open('README.md').read()),
    url="https://github.com/Ceasar/twosheds",
    author="Ceasar Bautista",
    author_email="cbautista2010@gmail.com",
    license='MIT',
    keywords=["twosheds", "shell"],
    packages=find_packages(),
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
