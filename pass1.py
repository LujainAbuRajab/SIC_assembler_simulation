"""Here I will build an assembler that translates SIC assembly language into machine code, and I have two passes 
Pass 1: Processes the source code, builds a symbol table, and generates an intermediate file.
we use the `prettytable` package  to create clean and readable ASCII tables in the terminal.
"""
 
from prettytable import PrettyTable


def file_reader(file):
    """read SIC program file.
    param file: file name that contain sic program
    return 2D array in form of -> [label, instruction, operand]
    """

    input_file = open(file,"rt") #read text mood
    data_file = []
    for line in input_file:
        if line[0] == ".":  # skip comment line
            continue
        # split to label, instruction, data && store in 2d array
        col = [line[0:10].strip(), line[12:20].strip(), line[22:39].strip()]
        data_file.append(col)

    input_file.close()
    return data_file

def opcode_reader():
    """ read instruction and opcode && store them in hash table.
    return optable in hash table( dictionary in python).
    """

    op_tabel = {} #Empty Dictionary -> instruction:opcode
    input_file = open('inst_set.txt', "rt")
    for line in input_file:
        op_tabel[line[0:10].strip()] = line[11:13].strip()
    input_file.close()
    return op_tabel