# -*- coding: utf-8 -*-

"""
rumps.compat
~~~~~~~~~~~~

Compatibility for Python 2 and Python 3 major versions.

:copyright: (c) 2020 by Jared Suttles
:license: BSD-3-Clause, see LICENSE for details.
"""

import sys

PY2 = sys.version_info[0] == 2


binary_type = bytes
text_type = str
string_types = (str,)

iteritems = lambda d: iter(d.items())
