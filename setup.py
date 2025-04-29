from setuptools import setup, find_packages

setup(
    # Info
    name='deskpal',
    author='Daniel Ervilha',
    version='0.1',
    # Package
    packages=find_packages(),
    install_requires=[],
    # Resources
    include_package_data=True,
    package_data={
        "deskpal": ["resources/**/*", "app/**/*"]
    }
)
