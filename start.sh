#!/bin/bash

DIRECTORY=".venv"
if [ -d "$DIRECTORY" ]; then
  pass
else
  echo "Can't found a venv. Creating"
  python3 -m venv .venv
  if [ $? -ne 0 ]; then
	  python -m venv .venv
  fi
fi
echo 'Found a venv'
source .venv/bin/activate
pip3 show arcade
if [ $? -ne 0 ]; then
	pip3 install arcade[full]
fi
echo 'Venv contain a valid arcade'


echo 'Running a game "Run from antivirus!"'
python3 main.py type='dialog'
if [ $? -ne 0 ]; then
	python main.py type='dialog'
fi
python3 main.py type='run'
if [ $? -ne 0 ]; then
	python main.py type='run'
fi
deactivate