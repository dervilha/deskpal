@echo off
python setup.py sdist bdist_wheel
echo Installing package...
pip install dist/deskpal-0.1-py3-none-any.whl --force-reinstall