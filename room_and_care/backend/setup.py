from setuptools import setup, find_packages

setup(
    name="room_and_care_backend",
    version="0.1",
    packages=find_packages(where="app"),
    package_dir={"": "app"},
    include_package_data=True,
)
