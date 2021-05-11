#!/bin/bash
set -e
DIR=/srv/soroban-csv-convert
LOG=/tmp/soroban.log

cd $DIR
. ./venv/bin/activate
nohup uvicorn main:app --reload --host 0.0.0.0 --port 5500 > $LOG &
