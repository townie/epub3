from setuptools import find_packages, setup

setup(
    name="epub3",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "lxml>=4.9.0",
        "defusedxml>=0.7.1",
        "pytz>=2022.1",
        "python-dateutil>=2.8.2",
    ],
    author="Author",
    author_email="author@example.com",
    description="An EPUB3 Library for reading, creating, and manipulating EPUB files",
    keywords="python,epub,epub3,ebook",
    url="https://github.com/username/epub3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
