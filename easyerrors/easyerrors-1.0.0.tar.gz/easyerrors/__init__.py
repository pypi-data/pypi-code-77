from dill.source import getsource
import inspect

def test(func):
	#Test out the given function and return any errors gracefully
	def innerfunc(*args, **kwargs):
		for i in range(0,len(args)):

			typ = type(args[i]).__name__
			if typ == 'str':
				exec(f"{inspect.getfullargspec(func)[0][i]} = '{args[i]}'")
			else:
				exec(f"{inspect.getfullargspec(func)[0][i]} = {typ}({args[i]})")

		# set vars
		sourcecode = getsource(func)
		errors = []
		lines = sourcecode.splitlines()

		# peform test
		print(f"\nTesting code inside function '{func.__name__}':")
		print('\n-------- Test started! --------\n')
		

		for line in lines:
			if '@' == line[0] or 'def ' == line[:4]:
				continue

			if '\t' == line[:1]:
				newline = line[1:]
			else:
				newline = line

			print(f">>> {newline}")
			try:
				try:
					eval(newline)
				except SyntaxError:
					exec(newline)

			except Exception as new_e:
				print(f"Error: {new_e}")
				errors.append(new_e)
			print('')



		print('\n-------- Test ended! --------')
		if errors:
			print('\n Errors found:')
			for e in errors:
				print(f"  - {e}")
			print('')

	return innerfunc		

print("Thanks for using the 'easyerrors' module! Go to 'pypi.org/projects/easyerrors/' for details.")