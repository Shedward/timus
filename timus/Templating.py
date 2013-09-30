
from os import path

def _add_to_each_line(src, add):
	return "\n".join([add + l for l in src.split('\n')])

def gen_tests_file(args):
	TESTS_TMPL = """
# Problem: {problem_id}. {problem_desc}
# Url: {url}
# Author: {name} ({id})

- Sample: 
    in: |
{test_input}
    out: |
{test_output}
"""
	args['test_input'] = _add_to_each_line(args['test_input'], ' '*8)
	args['test_output'] = _add_to_each_line(args['test_output'], ' '*8)
	return TESTS_TMPL.format(**args)


def template(srcfn, outfn, args, comment):
	TEMPL = """\
Problem: {problem_id}. {problem_desc}
Url: {url}
Author: {name} ({id})
Language: {lang_str} ({lang_descr})"""

	with open(srcfn, 'r') as srcf:
		src = srcf.read()

	header = _add_to_each_line(TEMPL.format(**args), comment)
	with open(outfn, 'w') as out:
		out.write("\n")
		out.write(header)
		out.write("\n")
		out.write(src)
		out.write("\n")

	# Generate tests file
	tests = gen_tests_file(args)
	testsfn = path.splitext(outfn)[0] + '.tests'
	with open(testsfn, 'w') as testsf:
		testsf.write(tests)

REGEX = {
	"lang":"Language: (\w{2,5})",
	"problem":"Problem: (\d{4})\.",
	"author": "Author: \(\w+\) (\w{6})"
}
def extract(filename):
	pass
