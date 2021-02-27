from sympy import *
import re
import multiprocessing
import os
import math

class Logic_expression():
    def __init__(self, logic_expression_string):
        self.logic_expression_string = logic_expression_string
        self._get_symbolic_expression()
        self._get_symbols()
        self._order_symbols()
        self._get_dnf()

    def _get_symbolic_expression(self):
        self.logic_expression_symbolic = parse_expr(self.logic_expression_string, evaluate = False)
    
    def _order_symbols(self):
        symbols_list_string = list(self.used_symbols.keys())
        symbols_list_string.sort()
        symbols_lib = {}
        for symbol_string in symbols_list_string:
            symbols_lib[symbol_string] = self.used_symbols[symbol_string]
        self.used_symbols = symbols_lib
        self.symbols_list = list(symbols_lib.values())
        
    def _get_symbols(self):
        symbol_lib = {}
        symbols_list = list(self.logic_expression_symbolic.atoms())
        for symbol in symbols_list:
            symbol_lib[str(symbol)] = symbols(str(symbol))
        self.used_symbols = symbol_lib

    
    def _get_truthtable(self):
        self.my_truthtable = Truth_table(self.logic_expression_symbolic, self.used_symbols)
        truthtable_full = self.my_truthtable.truth_table
        self.truthtable = {key:value for (key,value) in truthtable_full.items() if value == True}

    def _get_dnf_string(self):
        dnf_string = []
        true_terms = self.truthtable.keys()
        for true_term in true_terms:
            dnf_string.append(self._get_term_string(true_term))
        self.dnf_string = '|'.join(dnf_string)

    def _get_term_string(self, term):
        term_bin = ('{0:0'+str(len(self.used_symbols))+'b}').format(term)
        term_string = []
        for i in range(0,len(term_bin)):
            if int(term_bin[i]):
                term_string.append(str(self.symbols_list[i]))
            else:
                term_string.append('~'+ str(self.symbols_list[i]))
        return '('+ '&'.join(term_string) + ')'

    def _get_dnf(self):
        self._get_truthtable()
        self._get_dnf_string()

class Truth_table():
    def __init__(self, logic_expression_symbolic, symbols):
        self.logic_expression_symbolic = logic_expression_symbolic
        self.symbols = symbols
        self.symbols_string = list(self.symbols.keys())
        self._get_truth_table()
    
    def _create_table_entry(self, binary_i):
        symbol_dict = {}
        for i in range(0,len(self.symbols_string)):
            symbol_dict[self.symbols_string[i]] = binary_i[i]
        return symbol_dict

    def _evaluate_entry(self, tt_entry):
        return self.logic_expression_symbolic.subs(tt_entry)
        
    def _get_truth_table(self):
        truth_table_size = 2 ** (len(self.symbols))
        self.truth_table = {}
        for i in range(0,truth_table_size):
            binary_i = ('{0:0'+str(len(self.symbols))+'b}').format(i)
            tt_entry = self._create_table_entry(binary_i)
            self.truth_table[i] = self._evaluate_entry(tt_entry)

class Logic_expression_list():
    def __init__(self, full_expression_list):
        self.full_expression_list = full_expression_list
        self._process_parallel()

    def _expression_list_worker(self, part_expression_list,queue=None):
        result = {}
        for expression in part_expression_list:
            expression_instance = Logic_expression(expression)
            result[expression] = expression_instance.dnf_string
        if queue == None:
            return result
        else:
            queue.put(result)

    def _process_parallel(self):
        cpu_count = os.cpu_count()
        chunks_count = int(math.ceil(len(self.full_expression_list) / cpu_count))
        queue = multiprocessing.Queue()
        procs = []
        procs_range = range(0,min(cpu_count,len(self.full_expression_list)))
        for i in procs_range:
            proc = multiprocessing.Process(target=self._expression_list_worker, args=(self.full_expression_list[chunks_count*i:chunks_count*(i+1)], queue))
            procs.append(proc)
            proc.start()
        
        results ={}
        for i in procs_range:
            results.update(queue.get())
        
        for i in procs:
            i.join()
        self.results = results

def get_dnfs(string_List):
    my_Instance = Logic_expression_list(string_List)
    return(my_Instance.results)