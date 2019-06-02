@echo off
IF "%~1"=="" (
    echo "Missing parameter!"
    echo "Use run_local <microservice_name>"
    echo "Example: run_local metadata"
    exit
)

set ms=%~1
set pwd_path=%cd%
set PYTHONPATH=%pwd_path%;%PYTHONPATH%

python -c "import sys;print((hasattr(sys, \"real_prefix\") or (hasattr(sys, \"base_prefix\") and sys.base_prefix != sys.prefix)));"

for /f %%i in ('python -c "import sys;print((hasattr(sys, \"real_prefix\") or (hasattr(sys, \"base_prefix\") and sys.base_prefix != sys.prefix)));"') do (
    if "%%i" == "False" (
            python -m venv venv
            call ./venv/Scripts/activate
        goto :next
    )
)
:next

python -m pip install --upgrade pip
rem pip3 install --upgrade pip
pip3 install -r requirements.txt --upgrade
rem NLTK data will be installed in a virtual environment.
pip3 install chromedriver_installer --install-option="--chromedriver-version=2.29"
python ./googlesearch_downloadlink.py