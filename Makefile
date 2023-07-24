.PHONY: *

install: 
	python3 -m venv ./venv
	. ./venv/bin/activate && (\
		pip install --upgrade pip\
		pip install -r requirements.txt\
	)

run: 
	. ./venv/bin/activate && (\
		python redshifter.py\
	)

build:
	. ./venv/bin/activate && (\
		python setup.py build\
	)