from sczpy import say_hello
def test_encrytp():
    assert say_hello() == "Hello, World!"

def test_helloworld_with_param():
    assert say_hello("Everyone") == "Hello, Everyone!py"