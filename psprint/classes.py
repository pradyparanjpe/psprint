#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020 Pradyumna Paranjape
# This file is part of psprint.
#
# psprint is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# psprint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Classes
'''


from typing import Any
from colorama import Fore, Style


class InfoPrint():
    '''
    Fancy Print class that also prints the type of message
    '''
    def __init__(self) -> None:
        '''
        initialize print styles
        '''
        self.avail_colors = [
            Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
            Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
            Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
            Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX,
            Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX
        ]
        self.avail_styles = [Style.RESET_ALL, Style.NORMAL,
                             Style.DIM, Style.BRIGHT]
        self.info_list = [
            [0, 1, ""],
            [2, 1, 'inform'],
            [3, 1, 'action'],
            [4, 1, 'list'],
            [5, 1, 'warning'],
            [1, 1, 'error'],
            [6, 1, 'debug']
        ]
        self.max_info_size = 7
        self.info_style = []
        self._update_info_styles()

    def __str__(self) -> str:
        '''
        formatted InfoPrint().info_style
        '''
        outstr = 'info_style_index: color, style, info_type\n'
        for idx, info in enumerate(self.info_list):
            outstr += f'{idx}: {info[0]}, {info[1]}, {info[2]}\n'
        return outstr

    def _update_info_styles(self) -> None:
        '''
        update info styles based on available info lists
        '''
        for info_type in list(zip(*self.info_list))[-1]:
            self.max_info_size = max(self.max_info_size, len(info_type))
        for color, style, info in self.info_list:
            self.info_style.append(
                self.avail_colors[color] + self.avail_styles[style]
                + self._pad(info)
                + self.avail_styles[0]
            )

    def _pad(self, info) -> str:
        '''
        prepend spaces and [ ] to make it pretty
        '''
        return " " * (self.max_info_size - len(info)) \
            + "[" \
            + info.upper() + "] "

    def psprint(self, value: Any, i_t: Any = 0, **kwargs) -> None:
        '''
        value: prefixed with i_t and printed
        i_t: int: pre-declared info_type
        i_t: str: on-the-fly info_type (WHITE, NORMAL)

        everyting else is passed to print_function
        '''
        if isinstance(i_t, str):
            print(self._pad(i_t) + str(value), **kwargs)
            return
        if not 0 <= i_t < len(self.info_style):
            i_t = 0
        print(self.info_style[i_t] + str(value), **kwargs)
        return

    def add_style(self, info_type: str, color: int = 7, style: int = 1,
                  info_style_index: int = None) -> str:
        '''
        info_type: string prefixed to the line in the form [ INFO_TYPE ] STRING
        color: terminal color indices [0 - 15]
        style: Bright/Dim
        info_style_index: Index passed to psprint function as info_type

        Orders:
        colors: 0:BLACK\t1:RED\t2:GREEN\t3:YELLOW
                4:BLUE\t5:MAGENTA\t6:CYAN\t7:WHITE
                    and their Dim/Bright versions
        styles: 0:RESET_ALL\t1:NORMAL\t2:DIM\t3:BRIGHT

        returns the new (updated) info_style
        '''
        if not 0 <= color <= 15:
            raise ValueError("0 <= color <= 15")
        if 0 <= style <= 3:
            raise ValueError("0 <= style <= 3")
        if 0 <= len(info_type) <= 10:
            raise ValueError("Too long info type")
        if info_style_index is None or\
           info_style_index >= len(self.info_list):
            self.info_list.append([color, style, info_type])
        else:
            self.info_list.insert([color, style, info_type], info_style_index)
        self._update_info_styles()
        return str(self)

    def remove_style(self, info_style_index) -> str:
        '''
        info_style_index: is popped from the list

        returns the new (updated) info_style
        '''
        if info_style_index < len(self.info_list):
            self.info_list.pop(info_style_index)
        self._update_info_styles()
        return str(self)
