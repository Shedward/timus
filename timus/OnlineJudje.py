
import re
from time import sleep

import lxml.html
from requests import post

from timus.Exceptions import NetworkError, WrongParams
from timus.Logger import Log

BASE = "http://acm.timus.ru/"
URL = {
	"author": BASE+"author.aspx?id={id}",
	"problem": BASE+"problem.aspx?space=1&num={problem}",
	"status": BASE+"status.aspx?author={id}",
	"statusall": BASE+"status.aspx",
	"submit": BASE+"submit.aspx?space=1"
}

LANG_ID = {
	"cl": 9,
	"cl++": 10,
	"gcc": 20,
	"gcc11": 22,
	"g++": 21,
	"g++11": 23,
	"pas": 3,
	"ghc": 19,
	"go": 14,
	"c#": 11,
	"mono": 11,
	"java": 12,
	"py2": 16,
	"py3": 17,
	"rb": 18,
	"scala": 24,
	"vb": 15
}

def send(id, problem, file, lang):
	headers = {
		"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0"
	}
	
	if lang not in LANG_ID:
		raise WrongParams("Language {0} not supported.".format(lang))

	data = {
		'Action':'submit',
		'SpaceID': 1,
		'JudgeID': id,
		'Language': LANG_ID[lang],
		'ProblemNum': problem,
		'Source': ''
	}

	files = {'SourceFile':open(file, 'r')}

	request = post(url=URL['submit'], data=data, files=files,
				   headers=headers)
	return request

def get_name(id):
	html = lxml.html.parse(URL['author'].format(id=id[0:5]))
	name = html.xpath('//h2[@class="author_name"]/text()')[0]
	return name

def result_table(id):
	html = lxml.html.parse(URL['status'].format(id=id[0:5]))
	table = html.xpath('//table[@class="status"]')[0].findall('tr')
	data = []
	for row in table:
		data.append([c.text_content() for c in row.getchildren()])
	return data[2:-1]

def check_errors(r):
	if r.status_code != 200:
		raise NetworkError(r.status_code)

	# Check error message from acm.timus.ru
	reg = '(?<=Red;">).*?(?=</)' # Regex for red text
	m = re.search(reg, r.text)
	if m is not None:
		raise WrongParams(m.group())

	

def check_results(id, problem, timeout=1):
	LOG = Log()
	res = result_table(id)[0]
	stat = res[5]
	while stat in ['Compiling', 'Running', 'Waiting']:
		sleep(timeout)
		res = result_table(id)[0]
		stat = res[5]
		LOG(Log.Vrb, "\t", stat)
	return res

def format_msg(result):
	def insert(orig, new, pos):
		return orig[:pos] + new + orig[pos:]

	def replace(orig, frm, to):
		return [to if  x == frm else x for x in orig]

	if len(result) < 9:
		raise ValueError('Not enough elements in result list.')

	# Separate time and date stuck together
	if len(result[1]) > 9:
		result[1] = insert(result[1], ' ', 8)
	else:
		raise ValueError('Time is too short: ', result[1])

	# Mark empty lines with $DEL$
	rep_res = replace(result, '', '$DEL$')

	msg_tmpl = '''
 RESULTS:
	Solution: {0} 
	Time:     {1}
	Author:   {2}
	Problem:  {3}
	Language: {4}

	Time:     {7} s
	Memory:   {8}

	{5}
	Test:     {6}
	'''
	msg = msg_tmpl.format(*rep_res)

	# Remove all lines marked with $DEL
	is_not_have_del = lambda l : l.find('$DEL$') == -1
	return '\n'.join(filter(is_not_have_del, msg.split('\n')))

def submit(id, problem, file, lang):
	LOG = Log()
	LOG(Log.Msg, " :: Submiting")
	r = send(id, problem, file, lang)
	check_errors(r)
	LOG(Log.Msg, format_msg(check_results(id, problem)))