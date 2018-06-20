#!/usr/bin/env bash

set -x
set -e
set -u
set -o pipefail

SCRIPT_CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CHALLENGE_ID=$1
COVERAGE_TEST_REPORT_XML_FILE="${SCRIPT_CURRENT_DIR}/coverage.xml"
PYTHON_CODE_COVERAGE_INFO="${SCRIPT_CURRENT_DIR}/coverage.tdl"

# Install dependencies
pip install -r ${SCRIPT_CURRENT_DIR}/requirements.txt

# Compute coverage
( cd ${SCRIPT_CURRENT_DIR} && coverage run --source "lib/solutions" -m unittest discover -s test || true 1>&2 )
( cd ${SCRIPT_CURRENT_DIR} && coverage xml || true 1>&2 )

[ -e ${PYTHON_CODE_COVERAGE_INFO} ] && rm ${PYTHON_CODE_COVERAGE_INFO}

# Extract coverage percentage for target challenge
if [ -f "${COVERAGE_TEST_REPORT_XML_FILE}" ]; then
    COVERAGE_OUTPUT=$(xmllint --xpath '//package[@name="lib.solutions.'${CHALLENGE_ID}'"]/@line-rate' ${COVERAGE_TEST_REPORT_XML_FILE} || true)
    PERCENTAGE=$(( 0 ))
    if [[ ! -z "${COVERAGE_OUTPUT}" ]]; then
        NUMBER_AS_STRING=$(echo ${COVERAGE_OUTPUT} | cut -d "\"" -f 2 | tr -d "." | awk '{print $1}')
        PERCENTAGE=$(( 10#${NUMBER_AS_STRING} )) # Treat as base 10 number
    fi
    echo ${PERCENTAGE} > ${PYTHON_CODE_COVERAGE_INFO}
    cat ${PYTHON_CODE_COVERAGE_INFO}
    exit 0
else
    echo "No coverage report was found"
    exit -1
fi
