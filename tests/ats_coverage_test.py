# -*- coding: UTF-8 -*-

'''
Module
    ats_coverage_test.py
Copyright
    Copyright (C) 2024 - 2025 Vladimir Roncevic <elektron.ronca@gmail.com>
    ats_coverage is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    ats_coverage is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class ATSCoverageTestCase with attribute(s) and method(s).
    Creates test cases for checking functionalities of ATSCoverage.
Execute
    python3 -m unittest -v ats_coverage_test
'''

import sys
from typing import List
from unittest import TestCase, main

try:
    from ats_coverage import ATSCoverage
except ImportError as test_error_message:
    # Force close python test #################################################
    sys.exit(f'\n{__file__}\n{test_error_message}\n')

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2025, https://vroncevic.github.io/ats_coverage'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/ats_coverage/blob/dev/LICENSE'
__version__: str = '1.0.4'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class ATSCoverageTestCase(TestCase):
    '''
        Defines class ATSCoverageTestCase with attribute(s) and method(s).
        Creates test cases for checking functionalities of ATSCoverage.
        ATSCoverage unit tests.

        It defines:

            :attributes:
                | None
            :methods:
                | setUp - Call before test case.
                | tearDown - Call after test case.
                | test_default_create - Default on create (not None).
                | test_missing_args - Test missing args.
                | test_wrong_arg - Test wrong arg.
                | test_process - Generate code coverage for dummy project.
    '''

    def setUp(self) -> None:
        '''Call before test case.'''

    def tearDown(self) -> None:
        '''Call after test case.'''

    def test_default_create(self) -> None:
        '''Default on create (not None)'''
        generator: ATSCoverage = ATSCoverage()
        self.assertIsNotNone(generator)

    def test_missing_args(self) -> None:
        '''Test missing args'''
        sys.argv.clear()
        generator: ATSCoverage = ATSCoverage()
        self.assertFalse(generator.process())

    def test_wrong_arg(self) -> None:
        '''Test wrong arg'''
        sys.argv.clear()
        sys.argv.insert(0, '-d')
        sys.argv.insert(1, './pro')
        sys.argv.insert(0, '-p')
        sys.argv.insert(1, './pro/README.md')
        generator: ATSCoverage = ATSCoverage()
        self.assertFalse(generator.process())

    def test_process(self) -> None:
        '''Generate code coverage for dummy project'''
        sys.argv.clear()
        sys.argv.insert(0, '-n')
        sys.argv.insert(1, 'codecipher')
        sys.argv.insert(0, '-d')
        sys.argv.insert(1, './pro')
        sys.argv.insert(2, '-r')
        sys.argv.insert(3, './pro/README.md')
        generator: ATSCoverage = ATSCoverage()
        self.assertTrue(generator.process())


if __name__ == '__main__':
    main()
