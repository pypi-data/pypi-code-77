import pyperclip

def copy_table2(headers, *args):
    '''
    Creates a formated table based on headers and collumns
    :param headers : array
        names of each collumn
    :param *args : arrays
        collumns with data
    '''

    num_cols = 'c' * len(headers)
    collumns = args

    # Initialize table
    table = "\\begin{table}[!htbp]\n"
    table += "\t\centering\n"
    table += "\t\\begin{tabular}{" + f"{num_cols}" + "}\n"

    # Add headers
    table += "\t\t\hline\n"
    table += "\t\t" + ' & '.join(headers) + ' \\\\\n'
    table += "\t\t\hline\n"

    # Add collumns
    for row in range(len(collumns[0])):
        table += f"\t\t{collumns[0][row]} "
        for col in range(1, len(collumns)):
            table += f"& {collumns[col][row]} "
        table += "\\\\\n"
    table += "\t\t\hline\n" 

    # End table
    table += "\t\end{tabular}\n"
    table += "\t\caption{Caption here}\n"
    table += "\t\label{tab:label}\n"
    table += "\end{table}"

    pyperclip.copy(table)
    print("Table successfully copied to clipboard.")