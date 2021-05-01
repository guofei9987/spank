from abc import ABC

from pandas._typing import Axes, Axis, Dtype, FilePathOrBuffer, Level, Renamer
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    FrozenSet,
    Hashable,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)
import pandas
from spank.functions import Value
import re

regex = re.compile('(\w*)\s+(as|AS|As)\s+(\w*)')

Series = pandas.core.series.Series


class DistinctDict(dict):
    def __init__(self):
        super(DistinctDict, self).__init__()
        self.num = 0

    def get_num(self):
        self.num += 1
        return self.num

    def distinct_add(self, add_key, add_value):
        if add_key is None:
            add_key = '_unnamed_{}'.format(self.get_num())
        if add_key in self:
            raise KeyError("Duplicate columns names")
        else:
            self[add_key] = add_value


def tidy_select_col_str_expr(col_str):
    """
    col_str = 'col1 as col2'
    col_str = 'col1'
    :param col_str:
    :return:
    """
    m = regex.match(col_str)
    if m is not None:
        return m.group(3), m.group(1)
    else:
        return col_str, col_str


def tidy_select_expr(args, columns):
    cols1 = DistinctDict()
    for arg in args:
        if type(arg) is str:
            if arg == '*':
                for i in columns:
                    cols1.distinct_add(add_key=i, add_value=i)

            elif type(arg) is str:
                add_key, add_value = tidy_select_col_str_expr(col_str=arg)
                cols1.distinct_add(add_key=add_key, add_value=add_value)

        if type(arg) is Value:
            # 类似 F.Value(np.sin(sdf.col1)).alias('col3')
            if arg.alias_:
                cols1.distinct_add(add_key=arg.alias_, add_value=arg.v)
            else:
                cols1.distinct_add(add_key=None, add_value=arg.v)

        if type(arg) is Series:
            cols1.distinct_add(add_key=None, add_value=arg)

    return cols1


class DataFrame(pandas.DataFrame, ABC):
    def __init__(
            self,
            data=None,
            index: Optional[Axes] = None,
            columns: Optional[Axes] = None,
            dtype: Optional[Dtype] = None,
            copy: bool = False,
    ):
        super().__init__(data=data, index=index, columns=columns, dtype=dtype, copy=copy)

    def select_expr(self, *args):
        sdf_new = DataFrame()
        cols = tidy_select_expr(args=args, columns=self.columns)

        for alias_, col_ in cols.items():
            if type(col_) is str:
                sdf_new.loc[:, alias_] = self.loc[:, col_]
            else:
                sdf_new.loc[:, alias_] = col_

        return sdf_new

    def filter_expr(self, filter_conditions):
        return self.loc[filter_conditions, :]


