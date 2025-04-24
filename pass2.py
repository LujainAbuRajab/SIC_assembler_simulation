# Pass 2: Use the intermediate file(from pass 1) to produce the final object code and listing file.
''' processing: Inst -> generate its object code.
              Dir  -> handling 
              START, END  -> header and end records.'''
# for running the file: python pass2.py intermediate.mdt object.obj 

from prettytable import PrettyTable
import sys 

def file_reading(file):
    """read intermediate  file.
    :file: file that contain intermediate
    :return: 2D array include -> [location,label,instruction or directive,operand]
    """

    inputFile = open(file, "rt")
    dataFile = []
    for line in inputFile:
        # split each line to location, label, instruction,data && store in 2D array
        col = [line[0:9].strip(), line[10:26].strip(), line[27:43].strip(), line[44:60].strip()]
        dataFile.append(col)

    inputFile.close()
    return dataFile

def tab_read(file):
    """read file and store data in hash table.
    :return: optable and symtab in hash table.
    """

    _tabel = {}
    inputFile = open(file, "rt")
    for line in inputFile:
        _tabel[line[0:10].strip()] = line[11:15].strip()

    inputFile.close()
    return _tabel

def write_file(item, out, object):
    """write to the listing file
       :item: array [location ,label ,instruction and operand] from intermediate file.
       :out: list file to write in.
       :object: string -> object code."""
    
    for i in item:
        blanks = 15 - len(i)
        out.write(i + " " * blanks)

    out.write(object + "\n")


def text_record(list, out, add):
    """write text record in the object file
        :list: array contain objects code in text record
        :out: list file to write in.
        :add: address for text record.""" 
    
    length = hex(len(list) * 3)[2:]
    
    for i in list:
        if len(i) > 6:
            length = hex(int(length, 16) + int((6 - len(i)) / 2))[2:]
        elif len(i) < 6:
            length = hex(int(length, 16) - int((6 - len(i)) / 2))[2:]
    out.write('T^' + add + '^' + length)
    for i in list:
        out.write('^' + i)

    out.write('\n')



def pass_2(intermediate, obtab, symtab, listing_name, object_name):
    """write in the listing file
        :intermediate: array [location ,label ,instruction and operand] from intermediate file.
        :obtab: dictionary for inst. and there obcode.
        :symtab: dictionary for symbol and there loc. in program.
        :return: error_list -> list errors in program."""
    
    error_array = []  # array for errors in the code
    text_array = []  # array for text records
    object_code = ''

    # open files(listing + symbol)
    list = open(listing_name, "w")
    object1 = open(object_name, "w")
    directives = ["START", "END", "BYTE", "WORD", "RESB", "RESW"]
    length = hex(int(int(intermediate[len(intermediate) - 1][0], 16) - int(intermediate[0][3], 16)))[2:]
    
    if intermediate[0][2] != "START":  # handel error in `START` line
        print("\033[1;31m"+"An error in pass one!!")
        return 0
    elif intermediate[len(intermediate) - 1][2] != "END":  # handel error in `END` line
        print("\033[1;31m"+"An error in pass one!!")
        return 0
    else:
        text_address = intermediate[0][0]  # first location in text record

        for item in intermediate:

            if (len(text_array) > 9 or (item[2] == 'RESW') or (item[2] == 'RESB') or item[2] == 'END') and len(
                    text_array) > 0:  # (if text record have more than 9 inst. || address not continues print text record).
                text_record(text_array, object1, text_address)
                text_array = []  # clear array after print text record
                text_address = item[0]  # clear address

            if item[2] == 'START':
                object1.write("H^" + item[1] + "^" + item[3] + "^" + length + '\n')  # print header record.
                object_code = ""

            elif item[2] == 'END':
                object1.write("E^" + symtab[item[3]] + '\n')
                object_code = ""
                write_file(item, list, object_code)
                break
            
            elif item[2] == 'RSUB':
                object_code = obtab[item[2]] + "0000"

            elif item[2] in obtab.keys():

                if ',X' in item[3]:
                    if (item[3].replace(',X', "")) in symtab.keys():
                        operand = symtab[item[3].replace(',X', "")]
                        object_code = obtab[item[2]] + hex(int(operand[0], 16) + 8)[2:] + operand[1:]

                    else:
                        error_array.append("undefined symbol in line" + item[0])
                        object_code = obtab[item[2]] + "0000"

                else:
                    if item[3] in symtab:
                        object_code = obtab[item[2]] + symtab[item[3]]

                    else:
                        error_array.append("undefined symbol in line" + item[0])
                        object_code = obtab[item[2]] + "0000"

            elif item[2] in directives:
                if item[2] == 'WORD':
                    if item[3][0] == "-":
                        item[3] = item[3][1:]
                        if item[3].isdigit():
                            value = hex(((int(item[3]) * -1) + (1 << 24)) % (1 << 24))[2:]
                            item[3] = "-" + item[3]
                            object_code = ('0' * (6 - len(value))) + value
                    elif item[3].isdigit():
                        value = hex(int(item[3]))[2:]
                        object_code = ('0' * (6 - len(value))) + value
                    else:
                        error_array.append("error in " + item[2] + " you cant using word with string it should be "
                                                                   "integer!!!")

                elif item[2] == 'BYTE':
                    if item[3][0] == 'X':
                        object_code = item[3][2:-1]
                    elif item[3][0] == 'C':
                        object_code = item[3][2:-1].encode("utf-8").hex()

                else:
                    if item[3].isdigit():
                        object_code = ""
                        if item[2] == 'RESW':
                            text_address = hex(int(text_address, 16) + (int(item[3]) * 3))[2:]

                        else:
                            text_address = hex(int(text_address, 16) + (int(item[3])))[2:]

                    else:
                        error_array.append("error in " + item[2] + " you cant reserve a string value!!!")
            else:
                error_array.append("undefined instruction in line" + item[0])

            write_file(item, list, object_code)
            if object_code != '':
                text_array.append(object_code)
    list.close()
    object1.close()
    return error_array

    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python pass2.py <intermediate_file.mdt> <object_file.obj>")
        sys.exit(1)

    intermediate_filename = sys.argv[1]
    object_filename = sys.argv[2]
    listing_filename = "listing.lst"

    intermediate = file_reading(intermediate_filename)
    optable = tab_read('inst_set.txt')
    symtable = tab_read('symbol.txt')
    error_list = pass_2(intermediate, optable, symtable, listing_filename, object_filename)

    