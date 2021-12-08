from setuptools import setup, find_packages

setup(
    name="car-detector",
    version="2.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    license="MIT license",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["car_detector = app.__main__:car_detector"]},
    include_package_data=True,
)
