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
    Defines class VernamDecode with attribute(s) and method(s).
    Creates decode class with backend API.
'''

from dataclasses import dataclass, field
from typing import List, Optional

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://electux.github.io/codecipher'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/electux/codecipher/blob/main/LICENSE'
__version__ = '1.4.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass
class VernamDecode:
    '''
        Defines class VernamDecode with attribute(s) and method(s).
        Creates decode class with backend API.

        It defines:

            :attributes:
                | _decode_data - Data decode container.
            :methods:
                | decode_data - Property methods for decode data.
                | decode - Decode data from Vernam format.
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

    def decode(self, data: Optional[str], key: Optional[str]) -> None:
        '''
            Decoding data from Vernam format.

            :param data: Data which should be decoded | None
            :type data: <Optional[str]>
            :param key: Key for decoding | None
            :type key: <Optional[str]>
            :return: None
            :exceptions: None
        '''
        if bool(data) and bool(key):
            decode_list: List[str] = []
            key = (key * (len(data) // len(key))) + key[:len(data) % len(key)]
            for i, element in enumerate(data):
                if element.isalpha() and key[i].isalpha():
                    key_code: int = ord(key[i].lower()) - 96
                    code: int = ord(element.lower()) - 96
                    ans: int = code - key_code + 1
                    if ans < 1:
                        ans += 26
                    if element.isupper():
                        decode_list.append(chr(ans + 96).upper())
                    else:
                        decode_list.append(chr(ans + 96))
                else:
                    decode_list.append(element)
            self._decode_data = ''.join(decode_list)
