
from os import path
import re
from time import sleep
import pkg_resources

import lxml.html
from requests import post

from timus.Exceptions import NetworkError, OnlineJudje
from timus.Templating import template
from timus.TimusCompilers import lang_description, ext_by_lang
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
        raise OnlineJudje("Language {0} not supported.".format(lang))

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

def result_table(id):
    html = lxml.html.parse(URL['status'].format(id=id[0:5]))
    table = html.xpath('//table[@class="status"]')[0].findall('tr')
    data = []
    for row in table:
        data.append([c.text_content() for c in row.getchildren()])
    return data[2:-1]

def check_errors(html):
    # Check error message from acm.timus.ru
    mpos = html.find('color:Red')
    if mpos > -1: # Extract red text
        spos = html.find('>', mpos) + 1
        epos = html.find('</', spos)
        raise OnlineJudje(html[spos:epos])

    

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
    if r.status_code != 200:
        raise NetworkError(r.status_code)
    check_errors(r.text)
    LOG(Log.Msg, format_msg(check_results(id, problem)))

def get_name(id):
    html = lxml.html.parse(URL['author'].format(id=id[0:5]))
    name = html.xpath('//h2[@class="author_name"]/text()')[0]
    return name

def get_problem_data(problem):
    res = {}

    url = URL['problem'].format(problem=problem)
    res['url'] = url
    html = lxml.html.parse(url)

    check_errors(lxml.html.tostring(html).decode())

    problem_title = html.xpath('//h2[@class="problem_title"]/text()')[0]
    (problem_id, problem_desc) = map(str.strip, problem_title.split('.', 1))
    res['problem_id'] = problem_id
    res['problem_desc'] = problem_desc

    tests_table = html.xpath('//pre[@class="intable"]/text()')
    tests = zip(tests_table[::2], tests_table[1::2])

    res['tests'] = tests
    return res

def comment_by_ext(ext):
    if ext in ['cpp', 'c', 'pas', 'cs', 'go', 'java', 'scala']:
        return ' // '
    elif ext in ['py', 'rb', 'tests']:
        return ' # '
    elif ext == 'hs':
        return ' -- '

def init(problem, id, lang, templatefn=None, filename=None):
    LOG = Log()
    LOG(Log.Msg, " :: Getting problem")
    data = {
        'name': get_name(id),
        'id' : id,
        'lang_str' : lang,
        'lang_descr' : lang_description(lang)}
    data.update(get_problem_data(problem))

    MSG="\t{problem_id}. {problem_desc}\n\t{url}\n"
    LOG(Log.Msg, MSG.format(**data))

    ext = ext_by_lang(lang)
    comment_start = comment_by_ext(ext)
    if templatefn is None:
        templatefn = pkg_resources.resource_filename('templates','template.'+ ext)
    if filename is None:
        filename = (data['problem_id']+'.'+data['problem_desc'] + '.' + ext).replace(' ', '_')
    template(templatefn, filename, data, comment_start)
    LOG(Log.Msg, " :: Сreated")
    LOG(Log.Msg, "\t"+filename)
    LOG(Log.Msg, "\t"+path.splitext(filename)[0] + '.tests')
