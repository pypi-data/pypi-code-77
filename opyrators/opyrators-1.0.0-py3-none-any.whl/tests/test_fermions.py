import unittest
import sys
sys.path.append("..")
from opyrators.fermions import operator

class optermTest(unittest.TestCase):
    def setUp(self):
        return

    def test_operator_addition(self):
        A = operator({"112233":0.2})
        B = operator({"112230":1.3})
        C = A - B

        # Make sure A and B didn't change
        self.assertEqual(A.terms["112233"],0.2)
        self.assertEqual(B.terms["112230"],1.3)
        # Check resulting operator
        self.assertEqual(C.terms["112233"], 0.2)
        self.assertEqual(C.terms["112230"], -1.3)

    def test_identical_operator_addition(self):
        A = operator({"112233":0.2})
        B = operator({"112233":1.3})
        C = A + B
        self.assertEqual(C.terms["112233"], 1.5)

    def test_identical_operator_subtraction(self):
        A = operator({"112233":0.2})
        B = operator({"112233":0.2})
        C = A - B
        self.assertEqual(len(C.terms), 0)

        # Check that multiplying with a zero operator results in zero
        D = A * C
        self.assertEqual(len(D.terms),0)

    def test_identical_operator_multiplication(self):
        A = operator({"010":1})
        B = operator({"010":1})
        C = A * B
        self.assertEqual(len(C.terms), 0)

    def test_cdagger_c_multiplication(self):
        A = operator({"010":1})
        B = operator({"020":1})
        C = A * B
        self.assertEqual(C.terms["030"], 1)

    def test_c_cdagger_multiplication(self):
        A = operator({"020":1})
        B = operator({"010":1})
        C = A * B
        self.assertEqual(C.terms["000"], 1)
        self.assertEqual(C.terms["030"], -1)

    def test_scalar_multiplication(self):
        # Test multiplication with scalar on left
        A = operator({"112233":1})
        B = 3.0*A
        print(B)
        self.assertEqual(B.terms["112233"], 3.0)

        # Test multiplication with scalar on right
        A = operator({"112233":1})
        B = A*2.7
        self.assertEqual(B.terms["112233"], 2.7)

    def test_conjugation(self):
        A = operator({"112233":3+0.723j})
        A = A.conj()
        self.assertEqual(A.terms["221133"],3-0.723j)

if __name__ == '__main__':
  unittest.main()
