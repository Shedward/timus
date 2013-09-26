
class TimusError(Exception):
	prefix = 'Timus error:'

	def __init__(self, *args):
		self.args = args

	def msg(self):
		return str(self.prefix) + '\n\t' + ' '.join(map(str, self.args))



class NetworkError(TimusError):
	prefix = 'Network error:'

class OnlineJudje(TimusError):
	prefix = 'Online judje error:'

class WrongParams(TimusError):
	prefix = 'Wrong parameter:'

class CompilationError(TimusError):
	prefix = 'Compiler return code:'

class SourceFileNotFound(TimusError):
	prefix = 'Source file not found:'

class TestFileNotFound(TimusError):
	prefix = 'Test file not found:'

class WrongLang(TimusError):
	prefix = 'Wrong language:'

class NotSupportedExt(TimusError):
	prefix = 'Not supported extension:'