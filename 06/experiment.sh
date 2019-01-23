#!/bin/bash

python play.py -t $* &
python record.py -t $1
python analyze.py

