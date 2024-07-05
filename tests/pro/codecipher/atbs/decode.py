# -*- coding: UTF-8 -*-

'''
Module
    decode.py
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
    Defines class AlephTawBetShinDecode with attribute(s) and method(s).
    Creates decode class with backend API.
'''

import sys
from dataclasses import dataclass, field
from typing import List, Optional

try:
    from codecipher.atbs.lookup_table import LOOKUP_TABLE
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://electux.github.io/codecipher'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/electux/codecipher/blob/main/LICENSE'
__version__ = '1.4.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass
class AlephTawBetShinDecode:
    '''
        Defines class AlephTawBetShinDecode with attribute(s) and method(s).
        Creates decode class with backend API.

        It defines:

            :attributes:
                | _decode_data - Data decode container.
            :methods:
                | decode_data - Property methods for decode data.
                | decode - Decode data from AlephTawBetShin format.
    '''

    _decode_data: Optional[str] = field(default=None)

    @property
    def decode_data(self) -> Optional[str]:
        '''
            Property method for getting decode data.

            :return: Decode data in str format | None
            :rtype: <Optional[str]>
            :exceptions: None
        '''
        return self._decode_data

    @decode_data.setter
    def decode_data(self, decode_data: Optional[str]) -> None:
        '''
            Property method for setting decode data.

            :param decode_data: Decoded data | None
            :type decode_data: <Optional[str]>
            :return: None
            :exceptions: None
        '''
        if bool(decode_data):
            self._decode_data = decode_data

    def decode(self, data: Optional[str]) -> None:
        '''
            Decoding data from AlephTawBetShin format.

            :param data: Data which should be decoded | None
            :type data: <Optional[str]>
            :return: None
            :exceptions: None
        '''
        if bool(data):
            decode_list: List[str] = []
            for element in data:
                decode_list.append(LOOKUP_TABLE[element])
            self._decode_data = ''.join(decode_list)
