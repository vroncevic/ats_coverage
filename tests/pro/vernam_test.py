# -*- coding: UTF-8 -*-

'''
Module
    vernam_test.py
Copyright
    Copyright (C) 2021 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    codecipher is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    codecipher is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class VernamTestCase with attribute(s) and method(s).
    Creates test cases for checking functionalities of Vernam.
Execute
    python3 -m unittest -v vernam_test
'''

import sys
import unittest
from typing import List, Optional

try:
    from codecipher.vernam import Vernam
except ImportError as test_error_message:
    # Force close python test #################################################
    sys.exit(f'\n{__file__}\n{test_error_message}\n')

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2024, https://electux.github.io/codecipher'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/electux/codecipher/blob/dev/LICENSE'
__version__: str = '1.4.7'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class VernamTestCase(unittest.TestCase):
    '''
        Defines class VernamTestCase with attribute(s) and method(s).
        Creates test cases for checking functionalities of Vernam.

        It defines:

            :attributes:
                | RAW_DATA - Raw text data for encoding.
                | ENC_SEQ - Expected encoded sequence.
                | raw_data - Object container data for encoding.
                | enc_sequence - Object container for encoded sequence.
                | enc_data - Encoded data.
                | dec_data - Decoded data.
                | cipher - Cipher object.
            :methods:
                | setUp - Call before test cases.
                | tearDown - Call after test cases.
                | test_vernam_encoding - Test for base encoding vernam.
                | test_vernam_decoding - Test for base decoding vernam.
    '''

    RAW_DATA: str = 'More Human Than Human01 Is Our Motto'
    ENC_SEQ: str = 'Doeh Tlmnq Fyaa Vgdaa01 Zs Rid Mbwha'

    def setUp(self) -> None:
        '''Call before test cases.'''
        self.raw_data: Optional[str] = VernamTestCase.RAW_DATA
        self.enc_sequence: Optional[str] = VernamTestCase.ENC_SEQ
        self.enc_data: Optional[str] = None
        self.dec_data: Optional[str] = None
        self.cipher: Optional[Vernam] = Vernam()

    def tearDown(self) -> None:
        '''Call after test cases.'''
        self.raw_data = None
        self.enc_data = None
        self.dec_data = None
        self.cipher = None

    def test_vernam_encoding(self) -> None:
        '''Test base encoding.'''
        if bool(self.cipher):
            self.cipher.encode(self.raw_data, 'randomrandomrandom')
            self.enc_data = self.cipher.encode_data
            self.assertEqual(self.enc_sequence, self.enc_data)

    def test_vernam_decoding(self) -> None:
        '''Test base decoding.'''
        if bool(self.cipher):
            self.cipher.encode(self.raw_data, 'randomrandomrandom')
            self.enc_data = self.cipher.encode_data
            self.cipher.decode(self.enc_data, 'randomrandomrandom')
            self.dec_data = self.cipher.decode_data
            self.assertEqual(self.raw_data, self.dec_data)


if __name__ == '__main__':
    unittest.main()
