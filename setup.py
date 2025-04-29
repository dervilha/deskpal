from setuptools import setup, find_packages

setup(
    name='deskpal',
    author='Daniel Ervilha',
    version='0.1',
    # package_dir={'': 'src'},
    # packages=find_packages(where='src'),
    packages=find_packages(),
    install_requires=[],
    # Resources
    include_package_data=True,
    package_data={
        "deskpal": [
            "resources/**/*",
        ]
    }
)
