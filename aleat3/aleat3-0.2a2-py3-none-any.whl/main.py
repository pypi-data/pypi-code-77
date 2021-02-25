from aleat3 import Aleatoryous, coinToBool, coinToBinary
from aleat3.output.colored import UNABLE

__all__ = ["main",
           "coin",
           "dice",
           "roulette"]

# Main demostration of Aleatoryous:
def main():
    # Based from Tests/aleatoryous.py
    a = Aleatoryous("aleatory.coin")
    print("coin " + str(a.single() in ["Head", "Tails"]))
    print("cointobinary " + str(coinToBinary(a.single()) in [0, 1]))
    print("cointobool " + str(coinToBool(a.single()) in [True, False]))
    a.changemode("aleatory.dice")
    print("dice " + str(a.single() in [0, 1, 2, 3, 4, 5, 6]))
    b = ["a", "b", "c"]
    a.changemode("aleatory.roulette", b)
    print("roulette " + str(a.single() in b))
    print("colorama output " + str(UNABLE))
    print("Done")

# coin():
def coin():
    c = Aleatoryous("aleatory.coin")
    cc = c.single()
    print("""coin single() result: %s
coinToBool function: %s
coinToBinary function: %s"""%(cc, coinToBool(cc), coinToBinary(cc)))

# dice():
def dice():
    d = Aleatoryous("aleatory.dice")
    print("dice single() result: %s"%d.single())

# roulette():
def roulette():
    l = ["Option 1", "Option 2", "Option 3"]
    print("Available options:")
    for ll in range(l):
        print(" %s"%l[ll])
    r = Aleatoryous("aleatory.roulette", l)
    print("roulette single(): %s"%r.single())
