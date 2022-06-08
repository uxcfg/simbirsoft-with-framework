#!/bin/bash
# Скрипт запуска CI в Jenkins
# shellcheck source=/dev/null
. "${VENV}"/bin/activate
pytest "${REPO_PATH}"/tests -k="${JOB_NAME}" --alluredir="${WORKSPACE}"/allure-results --clean-alluredir --continue-on-collection-errors
