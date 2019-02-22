import logging

class ColorFormatter(logging.Formatter):
	colors = {
		'reset'		:	'\u001b[0m',
		
		'NOTSET'	:	'\u001b[90m',
		'DEBUG'		:	'\u001b[34m',
		'INFO'		:	'\u001b[32m',
		'WARNING'	:	'\u001b[33m',
		'ERROR'		:	'\u001b[31m',
		'CRITICAL'	:	'\u001b[1;91m'
	}

	def format(self, record):
		c = ColorFormatter.colors[record.levelname]
		message = c + super(ColorFormatter, self).format(record) + ColorFormatter.colors['reset']
		return message

def get(name):
	l = logging.getLogger(name)
	if not l.hasHandlers():
		configure(l)
	return l

def configure(l):
	l.setLevel(logging.DEBUG)
	
	sh = logging.StreamHandler()
	sh.setLevel(logging.DEBUG)
	sh.setFormatter(ColorFormatter('[{name:-^5}] [{levelname:-<8}] : {message}', style='{'))
	l.addHandler(sh)
	
	return l
	
if __name__ == '__main__':
	print('Executing color test ...\n')
	for l,c in ColorFormatter.colors.items():
		print('{}[{}] the quick brown fox jumps over the lazy dog'.format(c,l))
	print(ColorFormatter.colors['reset'])
	
	print('Executing logger test ...\n')
	l = configure('LOG')
	for i in range(6):
		l.log(i*10, '[%d] the quick brown fox jumps over the lazy dog', i*10)
	print()
	
	print('Tests complete!')
