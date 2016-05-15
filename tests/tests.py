"""

Helpers for tests.

"""

import ast
from ast_decompiler import decompile
import difflib


def check(code):
    """Checks that the code remains the same when decompiled and re-parsed."""
    tree = ast.parse(code)
    new_code = decompile(tree)
    new_tree = ast.parse(new_code)
    dumped = ast.dump(ast.parse(code))
    new_dumped = ast.dump(new_tree)

    if dumped != new_dumped:
        print code
        print new_code
        for line in difflib.unified_diff(dumped.split(), new_dumped.split()):
            print line
        assert False, '%s != %s' % (dumped, new_dumped)


def assert_decompiles(code, result, **kwargs):
    """Asserts that code, when parsed, decompiles into result."""
    decompile_result = decompile(ast.parse(code), **kwargs)
    if result != decompile_result:
        print '>>> expected'
        print result
        print '>>> actual'
        print decompile_result
        print '>>> diff'
        for line in difflib.unified_diff(result.splitlines(), decompile_result.splitlines()):
            print line
        assert False, 'failed to decompile %s' % code