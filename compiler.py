import sys

### Functions
def lexicalAnalyzer():
    global code_line
    global code_index
    global code_file
    global flag_eof
    
    token_type = "NONE"

    current_char = ""
    next_char = code_file.read(1)
    current_code_index = code_index
    
    ## Checking if the file is empty
    if (next_char == ""):
        flag_eof = True
        return (token_type, 0, code_line, current_code_index)        
        
    ## Checking for white spaces
    while (next_char == " " or next_char == "\n" or next_char == "\t"):
        if (next_char == "\n"):
            code_line += 1
            code_index = 0
        next_char = code_file.read(1)
        code_index += 1
            
    ## Checking if there is identifier or keyword       
    if (next_char.isalpha()):
        current_char = next_char
        next_char = code_file.read(1)
        code_index += 1
            
        while (next_char.isalpha() or next_char.isdigit()):
            current_char += next_char
            next_char = code_file.read(1)
            code_index += 1
             
        if (current_char in keywords):
            token_type = "KEYWORD"
            return (token_type, current_char, code_line, current_code_index)
        else:
            token_type = "IDENTIFIER"
            return (token_type, current_char, code_line, current_code_index)
        
    ## Checking for number
    elif (next_char.isdigit()):
        current_char = next_char
        next_char = code_file.read(1)
        code_index += 1

        while (next_char.isdigit()):
            current_char += next_char
            next_char = code_file.read(1)
            code_index += 1

        if (next_char.isalpha()):
            print("Error in line " + str(code_line) + " and index " + str(current_code_index) + ": Letter \"" + next_char + "\" found after digits \"" + current_char)
        else:
            token_type = "NUMBER"
            return (token_type, current_char, code_line, current_code_index)

    elif (next_char == "#"):
        current_char = next_char
        next_char = code_file.read(1)
        code_index += 1

        if (next_char == "#"):
            current_char = next_char
            next_char = code_file.read(1)
            code_index += 1
                
            while (next_char != current_char and current_char == "#"):
                current_char = next_char
                next_char = code_file.read(1)
                code_index += 1
                
                if (next_char == "\n"):
                    code_line += 1
 
        elif (next_char.isalpha()):
                
            while (next_char.isalpha()):
                current_char += next_char
                next_char = code_file.read(1)
                code_index += 1
            
            if (current_char in keywords):
                token_type = "KEYWORD"
                return (token_type, current_char, code_line, current_code_index)
            else:
                print("Error in line " + str(code_line) + " and index " + str(current_code_index) + ": Not recognizing the value \"" + current_char + "\"")
        else:
            current_char = next_char
            next_char = code_file.read(1)
            code_index += 1
                
            if (next_char == "{"):
                current_char += next_char
                code_index += 1
                token_type = "GROUP"
                return (token_type, current_char, code_line, current_code_index)
            elif (next_char == "}"):
                current_char += next_char
                code_index += 1
                token_type = "GROUP"
                return (token_type, current_char, code_line, current_code_index)
    elif (next_char == "(" or next_char == ")"):
        current_char = next_char
        code_index += 1
        token_type = "GROUP"
        return (token_type, current_char, code_line, current_code_index)
    else:
        print("Error in line " + str(code_line) + " and index " + str(current_code_index) + ": Not recognizing the value \"" + current_char + "\"")

    ## The format of the return set is (token_type, value, line, index)
    return (token_type, 0, 0, 0)

### The main function for all processes
def startProcessing():
    while (flag_eof == False):
        lexicalAnalyzer()
    
### Main Program
if __name__ == "__main__":
    print("Start compiling")
    code_line = 1
    code_index = 1
    flag_eof = False
    
    keywords = ("main", "def", "#def", "#int", "global", "if",
                "elif", "else", "while", "print", "return",
                "input", "int", "and", "or", "not")

    code_file = open(sys.argv[1], "r")
    startProcessing()
    print("Finish compiling")
