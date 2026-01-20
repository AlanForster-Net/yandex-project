#!/bin/bash

echo 'Running a game "Run from antivirus!"'
python3 main.py type='dialog'
if [ $? -ne 0 ]; then
	python main.py type='dialog'
fi
python3 main.py type='run'
if [ $? -ne 0 ]; then
	python main.py type='run'
fi
