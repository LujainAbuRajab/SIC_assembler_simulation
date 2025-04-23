# Pass 2: Use the intermediate file(from pass 1) to produce the final object code and listing file.
''' processing: Inst -> generate its object code.
              Dir  -> handling 
              START, END  -> header and end records.'''

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
       :object: string -> object code.
       """
    for i in item:
        blanks = 15 - len(i)
        out.write(i + " " * blanks)

    out.write(object + "\n")