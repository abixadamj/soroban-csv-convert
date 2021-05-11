#!/bin/bash
set -e
LOG=/tmp/soroban.log

. ./venv/bin/activate
nohup uvicorn main:app --reload --host 0.0.0.0 --port 5500 > $LOG &
