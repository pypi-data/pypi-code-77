from easyerrors import test

@test
def tryout(msg, num):
	print(msg, num,)

tryout('hey', 3)

@test
def tryout_2(msg, num):
	print(msg, num)
	print(incorrectargument)

tryout_2('hey', 3)