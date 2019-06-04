#!/bin/sh

python3 -m venv venv
. ./venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt --upgrade
#pip3 install chromedriver_installer --install-option="--chromedriver-version=2.29"
python3 ./async_dl.py
