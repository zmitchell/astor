# -*- coding: utf-8 -*-
"""
Part of the astor library for Python AST manipulation.

License: 3-clause BSD

Copyright 2012 (c) Patrick Maupin
Copyright 2013 (c) Berker Peksag

"""

import warnings

from .code_gen import to_source  # NOQA
from .node_util import iter_node, strip_tree, dump_tree
from .node_util import ExplicitNodeVisitor
from .file_util import CodeToAst, code_to_ast  # NOQA
from .op_util import get_op_symbol, get_op_precedence  # NOQA
from .op_util import symbol_data
from .tree_walk import TreeWalk  # NOQA

__version__ = '0.6'


# DEPRECATED!!!

# These aliases support old programs.  Please do not use in future.

# NOTE: We should think hard about what we want to export,
#      and not just dump everything here.  Some things
#      will never be used by other packages, and other
#      things could be accessed from their submodule.

deprecated = """
get_boolop = get_binop = get_cmpop = get_unaryop = get_op_symbol  # NOQA
get_anyop = get_op_symbol
parsefile = code_to_ast.parse_file
codetoast = code_to_ast
dump = dump_tree
all_symbols = symbol_data
treewalk = tree_walk
codegen = code_gen
"""

exec(deprecated)

def deprecate():
    def wrap(deprecated_name, target_name):
        if '.' in target_name:
            target_mod, target_fname = target_name.split('.')
            target_func = getattr(globals()[target_mod], target_fname)
        else:
            target_func = globals()[target_name]
        msg = "astor.%s is deprecated.  Please use astor.%s." % (deprecated_name, target_name)
        if callable(target_func):
            def newfunc(*args, **kwarg):
                warnings.warn(msg, FutureWarning)
                return target_func(*args, **kwarg)
        else:
            class ModProxy:
                def __getattr__(self, name):
                    warnings.warn(msg, FutureWarning)
                    return getattr(target_func, name)
            newfunc = ModProxy()

        globals()[deprecated_name] = newfunc

    for line in deprecated.splitlines():
        line = line.split('#')[0].replace('=', '').split()
        if line:
            target_name = line.pop()
            for deprecated_name in line:
                wrap(deprecated_name, target_name)

deprecate()

del deprecate, deprecated
