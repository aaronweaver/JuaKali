#!/bin/bash

echo $WORKSPACE
# Set "fail on error" in bash
set -e

source /etc/profile.d/rvm.sh
. "/usr/local/rvm/scripts/rvm"

cd /opt/gauntlt
# Activate the python virtual environment
#. venv/bin/activate

gauntlt $JUAKALIINSTALL/security-tests/$1
