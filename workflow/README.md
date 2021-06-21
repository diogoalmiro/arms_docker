# workflow1.1

1. Activate virtual environment and install requiements
2. `$ cd exec/`
3. `$ python workflow.py inputFile.tiff`

# Pre-requirements

`libtesseract (>=3.04)`
`libleptonica (>=1.71)`

To install them (on debian): `$ apt-get install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config`

# Virtual Environment
- To create an virtual environment: `$ python3 -m venv env`. (Only need to do once)
- To activate it: `$ source env/bin/activate`. (Every new terminal needs to activate)
- To install requirements: `$ pip install -r requirements` (Only need to do once)
- To save requirements: `$ pip freeze -r requirements` (To add new requirements)
