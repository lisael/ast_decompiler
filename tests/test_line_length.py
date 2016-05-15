from tests import assert_decompiles


def check_split(original, multiline, length_reduction=2):
    assert_decompiles(original, original, line_length=len(original))
    assert_decompiles(original, multiline, line_length=len(original.strip()) - length_reduction)


def test_indentation():
    assert_decompiles('''
if x:
    pass
''', '''if x:
 pass
''', indentation=1)


def test_with_prefix():
    prefixes = [
        'from x import',
        'import',
        'del',
        'global',
    ]
    for prefix in prefixes:
        check_split("%s a, b, c\n" % prefix, '''%s (
    a,
    b,
    c,
)
''' % prefix)


def test_boolop():
    check_split('if a and b and c:\n    pass\n', '''if (
    a and
    b and
    c
):
    pass
''', length_reduction=12)


def test_display():
    delimiters = [
        ('{', '}'),
        ('[', ']'),
        ('f(', ')'),
        ('\n\nclass Foo(', '):\n    pass')
    ]
    for start, end in delimiters:
        original = '%sa, b, c%s\n' % (start, end)
        assert_decompiles(original, original, line_length=len(original))

        assert_decompiles(original, '''%s
    a,
    b,
    c,
%s
''' % (start, end), line_length=len(start.lstrip()) + 5)


def test_assign():
    check_split('a, b, c = lst\n', '''(
    a,
    b,
    c,
) = lst
''', length_reduction=7)


def test_tuple():
    check_split('a, b, c\n', '''(
    a,
    b,
    c,
)
''')


def test_extslice():
    check_split('d[a:, b, c]\n', '''d[
    a:,
    b,
    c,
]
''')


def test_comprehension():
    check_split('[x for y in lst for x in y]\n', '''[
    x
    for y in lst
    for x in y
]
''')


def test_dict():
    check_split('{a: b, c: d}\n', '''{
    a: b,
    c: d,
}
''')


def test_dictcomp():
    check_split('{a: b for (a, b) in c}\n', '''{
    a: b
    for (a, b) in c
}
''')


def test_function_def():
    check_split('\ndef f(a, b, *args, **kwargs):\n    pass\n', '''
def f(
    a,
    b,
    *args,
    **kwargs
):
    pass
''', length_reduction=12)
