from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name='clothesline',
    version='0.1.0',
    author='Stefano Lottini',
    author_email='ultra',
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    # entry_points={
    #     "console_scripts": [
    #         "clothesline=clothesline:main",
    #     ],
    # },
    url='http://pypi.python.org/pypi/clothesline/',
    license='LICENSE.txt',
    description='An algebra for intervals over a range of continuous values',
    long_description=(here / "README.md").read_text(encoding="utf-8"),
    install_requires=[
        "requests",
        "pytest",
    ],
)