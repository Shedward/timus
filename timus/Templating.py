import re


def _add_to_each_line(src, add):
    return "\n".join([add + l for l in src.split('\n')])


def gen_source_file(srcfn, outfn, args, comment):
    TEMPL = """\
Problem: {problem_id}. {problem_desc}
Url: {url}
Author: {name} ({id})
Language: {lang_str} ({lang_descr})
Tests: {testsfn}"""

    with open(srcfn, 'r') as srcf:
        src = srcf.read()

    header = _add_to_each_line(TEMPL.format(**args), comment)
    with open(outfn, 'w') as out:
        out.write("\n")
        out.write(header)
        out.write("\n")
        out.write(src)
        out.write("\n")


def gen_tests_file(outfn, args):
    # Header
    res = """
# Problem: {problem_id}. {problem_desc}
# Url: {url}
# Author: {name} ({id})
""".format(**args)

    # Test intems
    TEST_TMPL = """
- Sample{i}:
    in: |
{inp}
    out: |
{out}"""
    tests = ""
    i = 0
    for inp, out in args['tests']:
        i += 1
        inp = _add_to_each_line(inp, ' '*8)
        out = _add_to_each_line(out, ' '*8)
        tests += TEST_TMPL.format(i=i, inp=inp, out=out)

    with open(outfn, 'w') as testsf:
        testsf.write(res)
        testsf.write(tests)


def extract(filename):
    with open(filename, 'r') as srcf:
        text = srcf.read()

    REGEXS = [
        ("lang", "Language:\s*([\w+#]*)\s"),
        ("problem", "Problem: (\d{4})\."),
        ("id", "Author: .* \((\w{7})\)"),
        ("tests", "Tests: (.*)")
    ]

    res = {}
    for k, reg in REGEXS:
        m = re.search(reg, text)
        if m is not None and len(m.groups()) > 0:
            res[k] = m.groups()[0]
    return res
