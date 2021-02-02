#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020 Pradyumna Paranjape
# This file is part of psprint.
#
# psprint is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# psprint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Text Parts

'''


import typing
from .ansi import ANSI


class AnsiEffect():
    '''
    Plain text object
    Text to be printed to (ANSI) terminal

    Args:
        color: color of text [0-15]
        gloss: gloss of text {0: bland, 1:normal ,2: dim, 3: bright}
        bgcol: color of background [0-15]

    Attributes:
        color: color of text
        gloss: gloss of text
        bgcol: background color
    '''
    def __init__(self,
                 color: str = ANSI.FG_COLOR[-1],
                 gloss: str = ANSI.GLOSS[1],
                 bgcol: str = ANSI.BG_COLOR[-1]) -> None:
        self.color = color
        self.gloss = gloss
        self.bgcol = bgcol

    @property
    def effects(self) -> str:
        '''
        All effects combined
        '''
        return self.color + self.bgcol + self.gloss

    @effects.setter
    def effects(self):
        '''
        Integrated effects (color, gloss, background)
        '''
        self.color = ''
        self.gloss = ''
        self.bgcol = ''

    @effects.deleter
    def effects(self):
        self.color = ''
        self.gloss = ''
        self.bgcol = ''

    @property
    def style_kwargs(self):
        '''
        extract color, gloss, bgcol to **kwargs
        '''
        return {'color': self.color,'gloss': self.gloss, 'bgcol': self.bgcol}

    def __copy__(self):
        '''
        create a copy
        '''
        return AnsiEffect(color=self.color, gloss=self.gloss, bgcol=self.bgcol)

    def __str__(self) -> str:
        '''
        Human readable form
        '''
        return self.effects

    def copy(self):
        '''
        method to create a copy
        '''
        return self.__copy__()


class PrintPref():
    '''
    Prefix that informs about Text

    Args:
        pref: str: prefix in long format
        short: str: prefix in short format
        pad_to: int: pad with `space` to length
        color: : color of text
        gloss: : gloss of text
        bgcol: : color of background

    Arguments:
        pref: tuple: prefix long, short
        pad: tuple: pad long, short
        effect: AnsiEffect: color/gloss effects

    '''
    def __init__(self, pref: str = '', short: str = '>', pad_to: int = 0,
                 **kwargs) -> None:
        self.effects = AnsiEffect(**kwargs)
        # 0: long, 1: short
        self.brackets = [1, 1]
        pad_max = (pad_to, 1)
        pad_len: typing.List[int] = [0, 0]
        self.pref = [pref.upper(), short.upper()]
        for idx, pref in enumerate(self.pref):
            if not pref:
                # pref is blank
                self.brackets[idx] = (0, 0)
                pad_len[idx] += 2  # corresponding to `[]`
            pad_len[idx]
            pad_len[idx] += max(pad_max[idx] - len(pref), 0)
        self.pad = [' ' * span for span in pad_len]

    def __copy__(self):
        '''
        create a copy
        '''
        new_copy = PrintPref()
        new_copy.effects = self.effects.copy()
        new_copy.pref = self.pref.copy()
        new_copy.pad = self.pad.copy()
        return new_copy

    def __len__(self) -> int:
        '''
        length of prefix
        '''
        return len(self.pref[0])

    def to_str(self, **kwargs) -> str:
        '''
        Print prefix with effects

        Args:
            short: prefix in short form?
            pad: Pad prefix
            bland: colorless pref
        '''
        pref_typ = int(kwargs.get('short'))  # 1 if short, else 0
        parts = {
            'ansi': '' if kwargs.get('bland') else str(self.effects),
            'text': self.pref[pref_typ],
            'brackets': self.brackets[pref_typ],
            'pref_pad': self.pad[pref_typ] if kwargs.get('pad') else ''
        }
        return ''.join([parts['ansi'],
                        '['* parts['brackets'],
                        parts['text'],
                        ']'* parts['brackets'],
                        parts['pref_pad'],
                        ANSI.RESET_ALL])
