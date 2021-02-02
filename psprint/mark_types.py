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
# GNU Lesser General Public License for more details. #
# You should have received a copy of the GNU Lesser General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Information Marker

'''

import warnings
from .ansi import ANSI
from .errors import KeyWarning, ValueWarning
from .text_types import PrintPref, AnsiEffect


DEFAULT_STYLE = {'color': 16, 'gloss': 1, 'bgcol': 16}
'''
Default Styles: white color, normal Gloss, black background
'''


'''
Maximum length of prefix. Prefix is padded to this length if called.
'''


class InfoMark():
    '''
    Prefix Mark information

    Attributes:
        pref: PrintPref: Prefix text properties
        text: PrintText: Text properties

    Args:
        parent: Inherit information from-
        pref: Message-description prefix
        pref_s: Short-description (1 character-long)
        pad_to: pad prefix to reach length
        pref_args: dict with keys: color, gloss, bgcol
        text_args: dict with keys: color, gloss, bgcol

    '''
    def __init__(self,
                 parent: 'InfoMark' = None,
                 pref: str = '',
                 pref_s: str = '>',
                 text_args: dict = {},
                 pref_args: dict = {},) -> None:
        if len(pref_s) > 1:
            trim = pref_s[:1]
            warnings.warn(
                "Prefix string '{pref_s}'" +
                f" is too long (length>1) trimming to {trim}",
                category=ValueWarning
            )
            pref_s = trim

        # Styles
        # inheritance:
        # Order of importance: kwargs ELSE parent ELSE default
        if parent is not None:
            pref_args = {**DEFAULT_STYLE,
                         **parent.pref.style_kwargs,
                         **pref_args}
            text_args = {**DEFAULT_STYLE,
                         **parent.text.style_kwargs,
                         **text_args}
            pref = pref or parent.pref.val
            pref_s = pref_s if pref_s != ">" else parent.pref.short
        else:
            pref_args = {**DEFAULT_STYLE, **pref_args}
            text_args = {**DEFAULT_STYLE, **text_args}

        self.pref = PrintPref(pref=pref, short=pref_s, pad_to=pref_max)
        self.text = AnsiEffect()
        # Settings
        self.pref.color = ANSI.FG_COLORS[pref_args['color']]
        self.pref.color = ANSI.BG_COLORS[pref_args['color']]
        self.pref.gloss = ANSI.GLOSS[pref_args['gloss']]

        self.text.color = ANSI.FG_COLORS[text_args['color']]
        self.text.color = ANSI.BG_COLORS[text_args['color']]
        self.text.gloss = ANSI.GLOSS[text_args['gloss']]

    def __str__(self) -> str:
        '''
        String format of available information
        '''
        return "\t".join(
            ("", self.pref.effects + self.pref.short,
             str(self.pref),
             self.text.effects + "<CUSTOM>" + ANSI.RESET_ALL)
        )

    def __copy__(self):
        '''
        Copy of instance
        '''
        child = InfoMark(pref=self.pref.val, pref_s=self.pref_s)
        child.pref = self.pref.__copy__()
        child.text = self.text.__copy__()
        return child

    def get_info(self) -> str:
        '''
        Print information

        '''
        info = str(self)
        print(info)
        return info
