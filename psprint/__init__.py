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
module init
'''


from .classes import InfoPrint


INFO_PRINT = InfoPrint()
psprint = INFO_PRINT.psprint
__all__ = [
    'InfoPrint',
    'INFO_PRINT',
    'psprint'
]
