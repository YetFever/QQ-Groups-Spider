"""
    pyexcel.plugins.sources.pydata
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of array, dict, records and book dict sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io.sheet import SheetReader

from pyexcel._compact import OrderedDict
from pyexcel._compact import zip_longest, PY2
import pyexcel.constants as constants


class _FakeIO(object):
    """emulates a stream object"""
    def __init__(self):
        self.__value = None

    def setvalue(self, value):
        """duck method setvalue"""
        self.__value = value

    def getvalue(self):
        """duck method getvalue"""
        return self.__value


# pylint: disable=W0223
class ArrayReader(SheetReader):
    """read data from an array via pyexcel-io interface"""

    def row_iterator(self):
        for row in self._native_sheet:
            yield row

    def column_iterator(self, row):
        for cell in row:
            yield cell


# pylint: disable=W0223
class RecordsReader(ArrayReader):
    """read data from a records via pyexcel-io interface"""

    def row_iterator(self):
        headers = []
        for index, row in enumerate(self._native_sheet):
            if index == 0:
                if isinstance(row, OrderedDict):
                    headers = row.keys()
                else:
                    headers = sorted(row.keys())
                yield list(headers)

            values = []
            for k in headers:
                values.append(row[k])
            yield values


# pylint: disable=W0223
class DictReader(ArrayReader):
    """read data from a dictionary via pyexcel-io interface"""

    def row_iterator(self):
        keys = self._native_sheet.keys()
        if not PY2:
            keys = list(keys)
        if not isinstance(self._native_sheet, OrderedDict):
            keys = sorted(keys)
        if self._keywords.get('with_keys', True):
            yield keys

        if isinstance(self._native_sheet[keys[0]], list):
            sorted_values = (self._native_sheet[key] for key in keys)
            for row in zip_longest(
                    *sorted_values,
                    fillvalue=constants.DEFAULT_NA):
                yield row
        else:
            row = [self._native_sheet[key] for key in keys]
            yield row
