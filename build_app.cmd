@echo off
pyinstaller --onefile --clean --name Deskpal --distpath deskpal/app/ deskpal/__main__.py