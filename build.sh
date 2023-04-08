#!/usr/bin/env bash
#exit on error

set -o errexit

pip install --upgrade pip
pip install python==3.9
pip install -r requirements.txt
