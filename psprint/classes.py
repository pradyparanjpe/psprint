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
Classes
'''

from sys import stdout
from warnings import warn
from typing import TypeVar
from colorama import Fore, Style, Back


StrInt = TypeVar("StrInt", str, int)


AVAIL_GLOSS = [Style.RESET_ALL, Style.NORMAL, Style.DIM, Style.BRIGHT]
FORE_COLORS = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
               Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
               Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
               Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX,
               Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX]
BACK_COLORS = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW,
               Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE,
               Back.LIGHTBLACK_EX, Back.LIGHTRED_EX, Back.LIGHTGREEN_EX,
               Back.LIGHTYELLOW_EX, Back.LIGHTBLUE_EX, Back.LIGHTMAGENTA_EX,
               Back.LIGHTCYAN_EX, Back.LIGHTWHITE_EX]
DEFAULT_STYLE = {'color': 7, 'gloss': 1, 'bgcol': 0}


class KeyWarning(Warning):
    '''
    Warning that a key was wrongly passed and has been interpreted as default
    '''
    pass


class ValueWarning(Warning):
    '''
    Warning that a key was wrongly passed and has been interpreted as default
    '''
    pass


class PrintText():
    '''
    Text to be printed to (ANSI) terminal
    '''
    def __init__(self, val='', color=Fore.WHITE,
                 gloss=Style.NORMAL, bgcol=Back.BLACK) -> None:
        '''
        Plain text object
        '''
        self.val = str(val)
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
    def effects(self, val) -> None:
        '''
        hard set effects
        '''
        self.color = ''
        self.gloss = ''
        self.bgcol = ''
        self.effects = val

    @effects.deleter
    def effects(self) -> None:
        '''
        return all effects as a single string
        '''
        self.color = ''
        self.gloss = ''
        self.bgcol = ''

    def __str__(self):
        '''
        print self
        '''
        return str(self.val)

    def __len__(self):
        '''length of value'''
        return len(self.val)


class PrintPref(PrintText):
    '''
    Prefix that informs about Text
    '''
    def __init__(self, val='', short='>', **kwargs) -> None:
        PrintText.__init__(self, val=val.upper(), **kwargs)
        self.short = short

class InfoMark():
    '''
    Information object
    '''
    def __init__(self, pref_long_str: str = '', pref_short_str: str = '>',
                 text_args: dict = {}, pref_args: dict = {},) -> None:
        '''
        pref_long_str: Message-description prefix
        pref_short_str: Short-description (1 character-long)
        pref_args: dict with keys: color, gloss, bgcol
        text_args: dict with keys: color, gloss, bgcol

        Initiate object
        '''
        # Standards check
        text_args = {**DEFAULT_STYLE, **text_args}
        pref_args = {**DEFAULT_STYLE, **pref_args}
        if len(pref_long_str) > 10:
            warn(f"Too long (>10) prefix string '{pref_long_str}', trimming",
                 category=ValueWarning)
            pref_long_str = pref_long_str[:10]

        if len(pref_short_str) > 1:
            warn(f"Short-prefix must be 1 character, trimming",
                 category=ValueWarning)
        # Styles
        self.pref = PrintPref(val=pref_long_str, short = pref_short_str)
        self.text = PrintText()

        # Settings
        self.pref.color = self._color_idx_2_obj(pref_args['color'])
        self.pref.bgcol = self._color_idx_2_obj(pref_args['bgcol'], back=True)
        self.pref.gloss = self._gloss_idx_2_obj(pref_args['gloss'])
        self.text.color = self._color_idx_2_obj(text_args['color'])
        self.text.bgcol = self._color_idx_2_obj(text_args['bgcol'], back=True)
        self.text.gloss = self._gloss_idx_2_obj(text_args['gloss'])

    def _color_idx_2_obj(self, color: StrInt = 7, back=False) -> str:
        '''
        convert color strings to corresponding integers
        '''
        if isinstance(color, int):
            if not 0 <= color <= 15:
                warn("0 <= color <= 15, using 7", category=KeyWarning)
                color = 7
        else:
            for idx, alias_tup in enumerate(
                    (
                        ('k',  '0',  'black'),
                        ('r',  '1',  'red'),
                        ('g',  '2',  'green'),
                        ('y',  '3',  'yellow'),
                        ('b',  '4',  'blue'),
                        ('m',  '5',  'magenta'),
                        ('c',  '6',  'cyan'),
                        ('w',  '7',  'white'),
                        ('lk', '8',  'light black'),
                        ('lr', '9',  'light red'),
                        ('lg', '10', 'light green'),
                        ('ly', '11', 'light yellow'),
                        ('lb', '12', 'light blue'),
                        ('lm', '13', 'light magenta'),
                        ('lc', '14', 'light ctan'),
                        ('lw', '15', 'light white'),
                    )
            ):
                if color in alias_tup:
                    color = idx
                    break
        if not isinstance(color, int):
            warn("Color string was not understood, fallback to default",
                 category=KeyWarning)
            color = 0 if back else 7
        return BACK_COLORS[color] if back else FORE_COLORS[color]

    def _gloss_idx_2_obj(self, gloss: StrInt = 1) -> str:
        '''
        convert gloss strings to corresponding integers
        '''
        if isinstance(gloss, int):
            if not 0 <= gloss <= 3:
                warn("0 <= gloss <= 3, using 1", category=KeyWarning)
                gloss = 1
        else:
            for idx, alias_tup in enumerate(
                    (
                        ('r',  '0',  'reset'),
                        ('n',  '1',  'normal'),
                        ('d',  '2',  'dim'),
                        ('b',  '3',  'bright'),
                    )
            ):
                if gloss in alias_tup:
                    gloss = idx
        if not isinstance(gloss, int):
            warn("Gloss string was not understood, defaulting to normal",
                 category=KeyWarning)
            gloss = 1
        return AVAIL_GLOSS[gloss]

    def __str__(self) -> str:
        '''
        string format of available information
        '''
        outstr = Style.RESET_ALL + '\tshort\tlong\ttext\n'
        outstr += Style.RESET_ALL + 'prefix:\t{}{}{}\t{}\t{}{}{}\n'.format(
            str(self.pref.color), str(self.pref.gloss),
            self.pref.short, self.pref,
            str(self.text.color), str(self.text.gloss),
            "<CUSTOM>" + AVAIL_GLOSS[0]
        )
        return outstr

    def get_info(self) -> str:
        '''
        This is defined only because flake8 complains that the object has
        only 1 public method

        print information
        '''
        print(str(self))
        return str(self)


class InfoPrint():
    '''
    Fancy Print class that also prints the type of message
    '''
    def __init__(self) -> None:
        '''
        initialize print styles
        '''
        # Standard info styles
        self.info_style = {
            'cont': InfoMark(pref_long_str="", pref_short_str=''),
            'info': InfoMark(pref_long_str="inform", pref_short_str='i',
                             pref_args={'color': 2}),
            'act': InfoMark(pref_long_str="action", pref_short_str='@',
                            pref_args={'color': 3}),
            'list': InfoMark(pref_long_str="list", pref_short_str='·',
                             pref_args={'color': 4}),
            'warn': InfoMark(pref_long_str="warning", pref_short_str='?',
                             pref_args={'color': 5}),
            'err': InfoMark(pref_long_str="error", pref_short_str='!',
                            pref_args={'color': 1, 'gloss': 3},
                            text_args={'color': 1, 'gloss': 2}),
            'bug': InfoMark(pref_long_str="debug", pref_short_str='#',
                            pref_args={'color': 6},
                            text_args={'color': 6, 'gloss': 2}),
        }
        self.max_info_size = 7
        self.info_index = ['cont', 'info', 'act', 'list', 'warn', 'err', 'bug']
        self.switches = {'pad': False, 'short': False,
                         'bland': False, 'disabled': False}
        self.print_kwargs = {'file': stdout, 'sep': "\t",
                             'end': "\n", 'flush': False}

    def __str__(self) -> str:
        '''
        formatted InfoPrint().info_style
        '''
        return "\n".join((f"{k}:{v}" for k, v in self.info_style.items()))

    def _prefix_mark(self, mark: InfoMark, **switches) -> str:
        '''
        mark: passed info mark
        index_str: string to call pref
        short: info_mark is in short form
        pad: Pad prefix
        bland: colorless pref
        disabled: Default python print function-like behaviour
        standard prefixed string
        '''
        switches = {**self.switches, **switches}
        pref: str = mark.pref.short if switches['short'] else mark.pref
        pref_out = self._prefix(pref, short=switches['short'], pad=switches['pad'])
        if switches['bland']:
            # Colorless output
            return pref_out
        return mark.pref.effects + pref_out + mark.text.effects

    def _prefix(self, pref: str, short: bool = None, pad: bool = None) -> str:
        '''
        prepend spaces and [ ] to make it pretty
        '''
        if short is None:
            short = self.switches['short']
        if pad is None:
            pad = self.switches['pad']
        preflen = len(pref)
        if not pref:
            preflen = - 2
        pad_len = 1 - preflen if short else self.max_info_size - preflen
        if pad_len < 0:
            pad_len = 0
        prefix = f"[{pref}]" if pref else ""
        padstr = " " + " " * pad_len
        return prefix + padstr * pad

    @staticmethod
    def _new_mark(**kwargs) -> InfoMark:
        '''
        Generate a new mark
        '''
        pref_args = {}
        for key, default in DEFAULT_STYLE.items():
            pref_args[key] = kwargs[f'pref_{key}'] if f'pref_{key}' in kwargs\
                else default
        text_args = {}
        for key, default in DEFAULT_STYLE.items():
            text_args[key] = kwargs[f'text_{key}'] if f'text_{key}' in kwargs\
                else default
        pref_long_str = kwargs.get('pref_long_str', '')
        pref_short_str = kwargs.get('pref_short_str', '>')
        return InfoMark(pref_long_str=pref_long_str,
                        pref_short_str=pref_short_str,
                        pref_args=pref_args, text_args=text_args)

    def _which_mark(self, pref: StrInt = None, **kwargs)-> InfoMark:
        '''
        Define a mark based on arguments supplied
        may be a pre-defined mark
        OR
        mark defined on the fly
        '''
        if pref is not None:
            # Pre-defined mark
            if isinstance(pref, int):
                if not 0 <= pref < len(self.info_index):
                    pref = 0
                return self.info_style[self.info_index[pref]]
            if isinstance(pref, str):
                return self.info_style.get(pref, self.info_style['cont'])
            else:
                raise TypeError(f"{pref} should be either str or int")
        return self._new_mark(**kwargs)

    def psprint(self, *args, pref: StrInt = None, **kwargs) -> None:
        '''
        *args: passed to print_function for printing
        pref: str/int: pre-declared InfoMark defaults: {
        cont: or 0 or anything else
        info: or 1
        act:  or 2
        list: or 3
        warn: or 4
        error:or 5
        bug:  or 6 } OR in **kwargs {
        pref_color: int/str (7)
        pref_gloss: int/str (1)
        pref_bgcol: int/str (0)
        text_color: int/str (7)
        text_gloss: int/str (1)
        text_bgcol: int/str (0)
        pref_long_str:  ""
        pref_short_str:  ">"
        }
        pad: if true, print with padding after pref
        short: if true, use {pref_short_str} instead
        bland: colorless
        disabled: behave like print_function
        file: passed to print function
        sep: passed to print function
        end: passed to print function
        flush: passed to print function
        '''
        if not args:
            print()
            return

        # Extract keys
        print_kwargs = {}
        for key, default in self.print_kwargs.items():
            print_kwargs[key] = kwargs[key] if key in kwargs else default

        switches = {}
        for key, default in self.switches.items():
            switches[key] = kwargs[key] if key in kwargs else default
        if switches['disabled']:
            print(*args, **print_kwargs)
            return

        args = list(args)
        mark = self._which_mark(pref=pref, **kwargs)
        args[0] = self._prefix_mark(mark=mark, **switches) + str(args[0])
        args[-1] = str(args[-1]) + Style.RESET_ALL
        print(*args, **print_kwargs)

    def edit_style(self, pref_long_str, index_handle: int = None,
                   index_str: str = None, **kwargs) -> str:
        '''
        index: Index handle that will call this InfoMark
        index_str: Index string handle that will call this InfoMark
        color: terminal color indices [0 - 15]
        gloss: Bright/Dim
        **kwargs: passed to InfoMark for initialization

        Orders:
        colors: 0:BLACK\t1:RED\t2:GREEN\t3:YELLOW
                4:BLUE\t5:MAGENTA\t6:CYAN\t7:WHITE
                    and their light versions
        styles: 0:RESET_ALL\t1:NORMAL\t2:DIM\t3:BRIGHT

        returns the new (updated) info_style
        '''
        if index_handle is None or \
           not 0 <= index_handle <= len(self.info_index):
            self.info_index.append(index_str)
        else:
            self.info_index.insert(index_handle, index_str)
        self.info_style[index_str] = \
            self._new_mark(pref_long_str=pref_long_str, **kwargs)
        return str(self)

    def remove_style(self, index_str: str = None,
                     index_handle: int = None) -> str:
        '''
        index_str: is popped out of defined styles
        index_handle: is used to locate index_str if it is not provided

        returns the new (updated) info_style
        '''
        if index_str is None:
            if index_handle < len(self.info_style):
                index_str = self.info_index.pop(index_handle)
        del self.info_style[index_str]
        return str(self)
