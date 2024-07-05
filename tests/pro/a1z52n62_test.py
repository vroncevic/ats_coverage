# -*- coding: UTF-8 -*-

'''
Module
    a1z52n62_test.py
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
    Defines class A1z52N62TestCase with attribute(s) and method(s).
    Creates test cases for checking functionalities of A1z52N62.
Execute
    python3 -m unittest -v a1z52n62_test
'''

import sys
import unittest
from typing import List, Optional

try:
    from codecipher.a1z52n62 import A1z52N62
except ImportError as test_error_message:
    # Force close python test #################################################
    sys.exit(f'\n{__file__}\n{test_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://electux.github.io/codecipher'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/electux/codecipher/blob/dev/LICENSE'
__version__ = '1.4.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class A1z52N62TestCase(unittest.TestCase):
    '''
        Defines class A1z52N62TestCase with attribute(s) and method(s).
        Creates test cases for checking functionalities of A1z52N62.

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
                | test_a1z52n62_encoding - Test for base encoding a1z52n62.
                | test_a1z52n62_decoding - Test for base decoding a1z52n62.
    '''

    RAW_DATA: str = 'More Human Than Human01 Is Our Motto'
    ENC_SEQ: List[str] = [
        '13', '42', '45', '32', ' ', '8', '48', '40', '28', '41', ' ',
        '20', '35', '28', '41', ' ', '8', '48', '40', '28', '41', '53',
        '54', ' ', '9', '46', ' ', '15', '48', '45', ' ', '13', '42',
        '47', '47', '42'
    ]

    def setUp(self) -> None:
        '''Call before test cases.'''
        self.raw_data: Optional[str] = A1z52N62TestCase.RAW_DATA
        self.enc_sequence: Optional[str] = ' - '.join(A1z52N62TestCase.ENC_SEQ)
        self.enc_data: Optional[str] = None
        self.dec_data: Optional[str] = None
        self.cipher: Optional[A1z52N62] = A1z52N62()

    def tearDown(self) -> None:
        '''Call after test cases.'''
        self.raw_data = None
        self.enc_data = None
        self.dec_data = None
        self.cipher = None

    def test_a1z52n62_encoding(self) -> None:
        '''Test base encoding.'''
        if bool(self.cipher):
            self.cipher.encode(self.raw_data)
            self.enc_data: Optional[str] = self.cipher.encode_data
            self.assertEqual(self.enc_sequence, self.enc_data)

    def test_a1z52n62_decoding(self) -> None:
        '''Test base decoding.'''
        if bool(self.cipher):
            self.cipher.encode(self.raw_data)
            self.enc_data = self.cipher.encode_data
            self.cipher.decode(self.enc_data)
            self.dec_data: Optional[str] = self.cipher.decode_data
            self.assertEqual(self.raw_data, self.dec_data)


if __name__ == '__main__':
    unittest.main()
