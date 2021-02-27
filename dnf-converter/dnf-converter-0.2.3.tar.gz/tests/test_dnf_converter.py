import unittest as ut
from dnf_converter.cli import main
from dnf_converter.dnf_converter import *
from sympy import *
import random

class TestDnfConverter(ut.TestCase):
    def test_main(self):
        assert main([]) == 0
    
    def test_Logic_expression(self):
        test_expression_string = '(A|B)&C'
        test_expression = Logic_expression(test_expression_string)
        assert test_expression.dnf_string == '(~A&B&C)|(A&~B&C)|(A&B&C)'

    def test_get_symbols_List(self):
        test_expression_string = '(A|B)&C'
        test_expression = Logic_expression(test_expression_string)
        assert test_expression.symbols_list == [symbols('A'),symbols('B'),symbols('C')]

    def test_get_symbols_symbols(self):
        test_expression_string = '(A|B)&C'
        test_expression = Logic_expression(test_expression_string)
        test_lib ={'A':symbols('A'),'B':symbols('B'),'C':symbols('C')}
        assert test_expression.used_symbols == test_lib

    def test_get_truthtable(self):
        test_expression_string = '(A|B)&C'
        test_expression = Logic_expression(test_expression_string)
        assert test_expression.truthtable == {3:True,5:True,7:True}

    def test_Truth_table(self):
        test_expression_string = '(A|B)&C'
        logic_expression_symbolic = parse_expr(test_expression_string, evaluate = False)
        symbol_dict = {'A':symbols('A'),'B':symbols('B'),'C':symbols('C')}
        test_truth_table = Truth_table(logic_expression_symbolic, symbol_dict)
        assert test_truth_table.truth_table == {0:False, 1:False, 2:False, 3:True, 4:False, 5:True, 6:False, 7:True}

    def test_create_table_entry(self):
        test_expression_string = '(A|B)&C'
        logic_expression_symbolic = parse_expr(test_expression_string, evaluate = False)
        symbol_dict = {'A':symbols('A'),'B':symbols('B'),'C':symbols('C')}
        test_truth_table = Truth_table(logic_expression_symbolic, symbol_dict)
        assert test_truth_table._create_table_entry('000') == {'A':'0','B':'0','C':'0'}
        assert test_truth_table._create_table_entry('010') == {'A':'0','B':'1','C':'0'}

    def test_evaluate_entry(self):
        test_expression_string = '(A|B)&C'
        logic_expression_symbolic = parse_expr(test_expression_string, evaluate = False)
        symbol_dict = {'A':symbols('A'),'B':symbols('B'),'C':symbols('C')}
        test_truth_table = Truth_table(logic_expression_symbolic, symbol_dict)
        assert test_truth_table._evaluate_entry({'A':'0','B':'0','C':'0'}) == False
        assert test_truth_table._evaluate_entry({'A':'1','B':'1','C':'1'}) == True

    def test_expression_list_worker(self):
        test_list = ['(A|B)&C','A&B','~A|B']
        worker = Logic_expression_list(test_list)
        result_list = worker._expression_list_worker(test_list)
        assert result_list == {'(A|B)&C': '(~A&B&C)|(A&~B&C)|(A&B&C)', 'A&B': '(A&B)', '~A|B': '(~A&~B)|(~A&B)|(A&B)'}

    def test_process_parallel(self):
        full_expression_list = ['(A|B)&C','A&B','~A|B']
        expr_List = Logic_expression_list(full_expression_list)
        assert expr_List.results == {'(A|B)&C': '(~A&B&C)|(A&~B&C)|(A&B&C)', 'A&B': '(A&B)', '~A|B': '(~A&~B)|(~A&B)|(A&B)'}
    
    def test_Masstest(self):
        number_of_teststrings = 20
        max_number_of_symbols = 10
        my_teststring_set = Teststringset(number_of_teststrings, max_number_of_symbols)
        my_teststrings = my_teststring_set.string_set
        expr_List = Logic_expression_list(my_teststrings)
        initial_string_List = list(expr_List.results.keys())
        for i in range(number_of_teststrings):
            string1 =  initial_string_List[i]
            string2 =  expr_List.results[string1]
            if len(string2):
                combined_string = '~' +'(' + string1  + ')'+ '&' +'(' + string2 + ')'
            else:
                continue
            print(combined_string)
            sub_dict = {}
            parsed_expression = parse_expr(combined_string)
            for sym in parsed_expression.atoms():
                sub_dict[sym] = random.randint(0,1)
            print(i)
            assert parsed_expression.subs(sub_dict) == False


class Teststringset():
    def __init__(self, number_of_teststrings, max_number_of_symbols):
        self.number_of_teststrings = number_of_teststrings
        self.max_number_of_symbols = random.randint(1,max_number_of_symbols)
        self._create_symbols()
        self._create_strings()

    def _create_symbols(self):
        self.symbols = []
        for i in range(0,self.max_number_of_symbols):
            self.symbols.append('sym'+str(i))

    def _create_strings(self):
        self.string_set = []
        for i in range(0,self.number_of_teststrings):
            self.available_symbols = self.max_number_of_symbols
            new_string = self._create_string()
            self.string_set.append(new_string)

    def _create_string(self, bracket_mode = False):
        expression_string = ''
        while self.available_symbols > 0:
            if random.randint(0,1): ##zufaellige not einfuegen
                expression_string = expression_string +'~'
            if not random.randint(0,3): ##Entscheigung ob neuer geklammerter ausdruck oder lediglich ein symbol eingesetzt werden soll
                bracket_string = self._create_string(bracket_mode=True)
                expression_string = expression_string + '(' + bracket_string + ')'
            else:
                expression_string = expression_string + random.choice(self.symbols) ##zufaellige variable auswaehlen
                self.available_symbols = self.available_symbols - 1 ##anzahl der verfuegbaren variablen verringern
            if random.randint(0,1): ## 'und' oder 'oder' einfuegen 
                expression_string = expression_string +'|'
            else:
                expression_string = expression_string +'&'

            if bracket_mode == True and not random.randint(0,2):
                break

        expression_string = expression_string[0:-1]
        return expression_string


if __name__=='__main__':
    ut.main()