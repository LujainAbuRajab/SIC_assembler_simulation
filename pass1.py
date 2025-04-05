""" Here I will build an assembler that translates SIC assembly language into machine code, and I have two passes 
Pass 1: Processes the source code, builds a symbol table, and generates an intermediate file.
we use the `prettytable` package  to create clean and readable ASCII tables in the terminal.
"""
 
from prettytable import PrettyTable


def file_reader(file):
    """ read SIC program file.
    :return: 2D array in form of -> [label, instruction, operand]
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

def optab_reader():
    """ read instruction and opcode && store them in hash table.
    :return: optable in hash table( dictionary in python).
    """

    op_tabel = {} #Empty Dictionary -> instruction:opcode
    input_file = open('inst_set.txt', "rt")
    for line in input_file:
        op_tabel[line[0:10].strip()] = line[11:13].strip()
    input_file.close()
    return op_tabel

def locctr(data, optab):
    """" pass1 assembler write in intermediate file as location,label,inst or directive ,operand.
    :parameter -> data : sic program that store in 2D array
    :parameter -> optab: opcode table in dictionary
    :return: Symbol table as dictionary
    """

    out = open("intermediate.mdt", "w")
    symtab = {}
    directives = ["START", "END", "BYTE", "WORD", "RESB", "RESW"]

    # Check if 'START' and 'END' instructions are valid
    if data[0][1] != "START":  
        print("you have an error in first line : where Start !!")
        return 0
    elif data[len(data) - 1][1] != "END": 
        print("you have an error in last line : where END !!")
        return 0
    else:
        print("\n Program Name   :" + data[0][0])
        print("Program Location   :" + data[0][2])
        first_location = data[0][2]
        Locctr = '0x' + data[0][2] #memory address in hex

        #process each line in the file
        for item in data:
            if item[0] != '':  # check if line contain label(not empty + not START) to add to symbol table
                if item[1] != "START": 
                    if item[0] in symtab.keys():
                        print('ERROR : duplicat Symbol ==> ' + item[0])
                        return 0
                    symtab[item[0]] = Locctr[2:] # symtab['FIRST'] = '1003', while 'Locctr[2:]' removes the `0x`
            inst = item[1]
            if inst in directives:
                blanks = 10 - len(Locctr[2:])  # write in intermediate file
                out.write(Locctr[2:] + " " * blanks)
                for i in item:
                    blanks = 17 - len(i)
                    out.write(i + " " * blanks)
                out.write("\n")

                if inst == 'WORD': # 3 bytes
                    Locctr = hex(int(Locctr[2:], 16) + 3)
                elif inst == 'RESW': # num of words * 3
                    count = item[2]
                    Locctr = hex(int(Locctr[2:], 16) + (int(count) * 3))
                elif inst == 'RESB': # num of bytes
                    count = item[2]
                    Locctr = hex(int(Locctr[2:], 16) + (int(count)))
                elif inst == 'BYTE':
                    if item[2][0] == 'X': # 1 byte/2 hex chars
                        Locctr = hex(int(Locctr[2:], 16) + int((len(item[2]) - 2) / 2))

                    elif item[2][0] == 'C': # 1 byte/char
                        Locctr = hex(int(Locctr[2:], 16) + (len(item[2]) - 3))
                    else:
                        print("invalid oprend in line "+Locctr)
                        return 0;
                elif inst == 'END':
                    print("Program Length   :" + hex(int(int(Locctr[2:], 16) - int(first_location,16)))[2:])

            elif inst in optab.keys():
                blanks = 10 - len(Locctr[2:])
                out.write(Locctr[2:] + " " * blanks)
                for i in item:
                    blanks = 17 - len(i)  # max operand length
                    out.write(i + " " * blanks)
                out.write("\n")
                Locctr = hex(int(Locctr[2:], 16) + 3)
            else:
                print("error this instruction is not valid!")
                return 0

        return symtab
    
if __name__ == '__main__':
    data = file_reader("SIC_file_ex1.txt")
    symbol = open("symbol.txt", "w")
    optab = optab_reader()
    table_list = []
    symtab = locctr(data, optab)
    if symtab == 0:  # check errors
        pass
    else:
        for i in range(len(symtab)):
            col = [list(symtab.items())[i][0], list(symtab.items())[i][1]]
            table_list.append(col)


        table = PrettyTable(['Symbol', 'Address'])  # using prettyTable library to arrange symbol table.
        for rec in table_list:
            table.add_row(rec)
            blanks = 11 - len(rec[0])
            symbol.write(rec[0] + " " * blanks + rec[1] + '\n')

        print("\n SYMBOL TABLE  :\n")
        print(table)

        symbol.close()