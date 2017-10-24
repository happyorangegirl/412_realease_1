#  Copyright 2016 EMC HCE SW Automation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from __future__ import print_function

# partially from package six by Benjamin Peterson

import sys
import os
import types

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    def utf8(s):
        return s


    def to_str(s):
        return s


    def to_unicode(s):
        return s

else:
    def utf8(s):
        return s.encode('utf-8')


    def to_str(s):
        return str(s)


    def to_unicode(s):
        return unicode(s)

if PY3:
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes

    MAXSIZE = sys.maxsize
    unichr = chr
    import io

    StringIO = io.StringIO
    BytesIO = io.BytesIO

else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str

    # to allow importing
    unichr = unichr  # type: ignore
    from StringIO import StringIO as _StringIO

    StringIO = _StringIO
    import cStringIO

    BytesIO = cStringIO.StringIO

if PY3:
    builtins_module = 'builtins'
else:
    builtins_module = '__builtin__'


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    return meta("NewBase", bases, {})


DBG_TOKEN = 1
DBG_EVENT = 2
DBG_NODE = 4

_debug = None


# used from yaml util when testing
def dbg(val=None):
    global _debug
    if _debug is None:
        # set to true or false
        _debug = os.environ.get('YAMLDEBUG')
        if _debug is None:
            _debug = 0
        else:
            _debug = int(_debug)
    if val is None:
        return _debug
    return _debug & val


def nprint(*args, **kw):
    if dbg:
        print(*args, **kw)
