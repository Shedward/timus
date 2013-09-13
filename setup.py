
from setuptools import setup
from os.path import join, dirname

setup(
	name='Timus',
	version='0.1.0',
	author='Vlad Maltsev',
	author_email='shedwardx@gmail.com',
	url='https://github.com/Shedward/timus',
	packages=["timus"],
	description="Console client for acm.timus.ru with simple in/out test framework",
	long_description=open(join(dirname(__file__), 'README.md')).read(),
	license=open(join(dirname(__file__),"LICENSE")).read(),
	scripts=['bin/timus'],
	test_suite='tests',
	install_requires=[
		'psutil >= 0.6.1',
		'PyYAML >= 3.10'
	]
)