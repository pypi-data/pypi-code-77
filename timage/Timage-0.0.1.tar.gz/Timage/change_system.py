# Created by Hayk_Sardaryan at 06.11.2020 / 20:41
from string import ascii_uppercase


class ChangeSystem:
    _35_symbols = {k: m for m, k in zip(ascii_uppercase, range(10, 36))}
    reversed_35_symbols = {m: k for m, k in zip(ascii_uppercase, range(10, 36))}

    def _system_to_dec(self, num: str, from_system: int) -> int:
        if 35 >= from_system:
            res = 0
            for i, n in enumerate(num[::-1]):

                # if abcdef then convert a,b,c,d,e,f, to 10,11,12,13,14,15
                if n.upper() in self.reversed_35_symbols:
                    res += self.reversed_35_symbols[n.upper()] * from_system ** i
                # end convert

                else:
                    res += int(n) * from_system ** i
            return res
        else:
            raise ValueError("from_system must be less or equal than 35")

    def _dec_to_system(self, num: int, to_system: int) -> str:
        if not (isinstance(num, int) and isinstance(to_system, int)):
            raise ValueError("Num and to_system must be int")
        # if

        if 35 >= to_system:
            res = []
            while num:
                last_dig = num % to_system
                if last_dig in self._35_symbols:
                    res.append(self._35_symbols[last_dig])
                else:
                    res.append(str(last_dig))
                num //= to_system

            return "".join(res[::-1])
        else:
            raise ValueError("to_system must be less or equal than 35")

    def __new__(cls, num: str, from_system: int = 10, to_system: int = 2, len_of_return_number: int = 5) -> str:
        if num == 0:
            return '0'
        self = object.__new__(cls)

        def change():
            a = cls._system_to_dec(self, num, from_system)
            b = cls._dec_to_system(self, a, to_system)
            if len(str(b)) < len_of_return_number:
                delta_length = len_of_return_number - len(str(b))
                return '0' * delta_length + str(b)
            return b

        max_num = 0
        for n in num:
            if n.upper() in self.reversed_35_symbols and self.reversed_35_symbols[n.upper()] > max_num:
                max_num = self.reversed_35_symbols[n.upper()]
            elif n.upper() not in self.reversed_35_symbols and n.isdigit() and int(n) > max_num:
                max_num = int(n)

        if max_num >= from_system:
            a = self._35_symbols[max_num]
            raise ValueError(f'Num must be less than from_system ({a}={max_num})<{from_system}')
        else:
            return change()
