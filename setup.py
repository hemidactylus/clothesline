from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name='clothesline',
    version='0.1.1',
    author='Stefano Lottini',
    author_email='sl_@fastmail.com',
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    # entry_points={
    #     "console_scripts": [
    #         "clothesline=clothesline:main",
    #     ],
    # },
    url='https://github.com/hemidactylus/clothesline',
    license='LICENSE.txt',
    description='An algebra for intervals over a range of continuous values',
    long_description=(here / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    # install_requires=[
    #     "pytest",
    # ],
    python_requires=">=3.4.*",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        #
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="sets, intervals, algebra",
)
