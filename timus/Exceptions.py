
class TimusError(Exception):
	prefix = 'Timus error:'
	postfix = ''

	def __init__(self, *args):
		self.args = args

	def msg(self):
		return str(self.prefix) + '\n\t' \
			   + ' '.join(map(str, self.args)) \
			   + '\n\n' + self.postfix



class NetworkError(TimusError):
	prefix = 'Network error:'

class OnlineJudje(TimusError):
	prefix = 'Online judje error:'

class WrongParams(TimusError):
	prefix = 'Wrong parameters:'
	postfix = "Use timus -h for help"

class CompilationError(TimusError):
	prefix = 'Compiler return code:'

class SourceFileNotFound(TimusError):
	prefix = 'Source file not found:'

class TestFileNotFound(TimusError):
	prefix = 'Test file not found:'
	postfix = 'Use -t option to define custom tests file'

class WrongLang(TimusError):
	prefix = 'Wrong language:'

class NotSupportedExt(TimusError):
	prefix = 'Not supported extension:'