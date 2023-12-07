from setuptools import setup, find_packages

setup(
    name="mynetcdf4",
    version="1.0.0",
    description="",
    author='Santiago Basañes',
    author_email='santi.basanes@gmail.com',
    url='https://github.com/tiagobasagh/mynetcdf4',
    packages=find_packages(include=["mynetcdf4", "mynetcdf4.*"]),
    install_requires=[
        "pandas",
        "munch", 
        "sqlalchemy",
        "pyodbc",
        "jinja2",
    ],
    setup_requires=["flake8", "black"],
)