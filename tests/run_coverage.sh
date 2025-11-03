#!/bin/bash
#
# @brief   ats_coverage
# @version v1.0.4
# @date    Fri Jul  5 09:44:18 PM CEST 2024
# @company None, free software to use 2024
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

rm -rf htmlcov ats_coverage_coverage.xml ats_coverage_coverage.json .coverage .executed_tests
python3 -m coverage run -m --source=../ats_coverage unittest discover -s ./ -p '*_test.py' -vvv
python3 -m coverage html -d htmlcov
python3 -m coverage xml -o ats_coverage_coverage.xml 
python3 -m coverage json -o ats_coverage_coverage.json
python3 -m coverage report --format=markdown -m

