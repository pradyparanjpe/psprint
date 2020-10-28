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
Prompt String-like Print
'''


import os
from pathlib import Path
from configparser import ConfigParser
from .classes import InfoPrint


DEFAULT_PRINT = InfoPrint()


def _set_opts(rcfile) -> None:
    '''
    infile: rc file to read
    '''
    conf = ConfigParser()
    conf.read(rcfile)
    for mark in conf:
        if mark == "FORM":
            DEFAULT_PRINT.short = conf[mark].get("short", False)
            DEFAULT_PRINT.pad = conf[mark].get("pad", False)
            DEFAULT_PRINT.flush = conf[mark].get("flush", False)
        else:
            DEFAULT_PRINT.edit_style(**conf[mark])


RC_LOCATIONS = {
    'user': Path(os.environ["HOME"]).joinpath("." + "psprintrc"),
    'local': Path(os.getcwd()).joinpath("." + "psprintrc"),
    'config': Path(os.environ["HOME"]).joinpath(
        ".config", "psprintrc", "style.conf"
    ),
    'xdg_config': Path().joinpath("psprintrc"),  # juvenile user|fails
    'root': Path("/etc/psprint/psprintrc/style.conf"),
}

try:
    RC_LOCATIONS['xdg_config'] = Path(
        os.environ["XDG_CONFOG_HOME"]
    ).joinpath("psprintrc", "style.conf")
except KeyError:
    pass


for loc in 'root', 'user', 'config', 'xdg_config', 'local':
    if RC_LOCATIONS[loc].exists():
        _set_opts(RC_LOCATIONS[loc])


PRINT = DEFAULT_PRINT.psprint
__all__ = [
    'InfoPrint',
    'DEFAULT_PRINT',
    'PRINT'
]
