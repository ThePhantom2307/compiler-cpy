from asyncio.windows_events import NULL
import sys

### Classes
class Token:
    def __init__(self, recognized_token, token_type, line_number):
        self.recognized_token = recognized_token
        self.token_type = token_type
        self.line_number = line_number
    
    def __str__(self):
        return(self.recognized_token + "\t family: " + self.token_type + "\t Line: " + str(self.line_number))


### Functions

## Lexical Analyzer 
def lexicalAnalyzer():
    global code_line
    global code_file
    global eof_flag
    
    token_type = "EOF"

    current_char = ''
    next_char = code_file.read(1)
    
    ## Checking if the file is empty
    if (not next_char):
        eof_flag = True
        return (token_type, 0, code_line)

    ## Checking for white spaces
    while (next_char == ' ' or next_char == '\n' or next_char == '\t'):
        if (next_char == '\n'):
            code_line += 1

        next_char = code_file.read(1)

        if (not next_char):
            eof_flag = True
            return (token_type, "", code_line)

    ## Checking for comments or open or closed brackets
    if (next_char == '#'):
        current_char = next_char
        next_char = code_file.read(1)

        if (next_char == '#'):
            current_char = next_char
            next_char = code_file.read(1)

            start_comment = code_line
            
            current_char = next_char
            next_char = code_file.read(1)

            while (next_char != '#' or current_char != '#'):
                if (next_char == '\n'):
                    code_line += 1
        
                if (not next_char):
                    print("Syntax error in line " + str(start_comment) + ": Comment section started but never closed")
                    sys.exit(0)
                    
                current_char = next_char
                next_char = code_file.read(1)
                
            return(lexicalAnalyzer())
            
        else:
            if (next_char.isalpha()):
                while (next_char.isalpha()):
                    current_char += next_char
                    next_char = code_file.read(1)
                
                code_file.seek(code_file.tell() - 1)
                
                if (current_char in keywords):
                    token_type = "KEYWORD"
                    return (token_type, current_char, code_line)
                else:
                    print("Syntax error in line " + str(code_line) + ": Not recognizing the value \"" + current_char + "\"")
                    sys.exit(0)
        
            elif (next_char == '{'):
                current_char += next_char
                token_type = "GROUP"
                return (token_type, current_char, code_line)
        
            elif (next_char == '}'):
                current_char += next_char
                token_type = "GROUP"
                return (token_type, current_char, code_line)
            
            else:
                print("Syntax error in line " + str(code_line) + ": Not recognizing the value \"" + current_char + "\"")
                sys.exit(0)
            
    ## Checking if there is identifier or keyword       
    elif (next_char.isalpha()):
        current_char = next_char
        next_char = code_file.read(1)
            
        while (next_char.isalpha() or next_char.isdigit()):
            current_char += next_char
            next_char = code_file.read(1)
        
        code_file.seek(code_file.tell() - 1)

        if (current_char in keywords):
            token_type = "KEYWORD"
            return (token_type, current_char, code_line)
        else:
            token_type = "IDENTIFIER"
            return (token_type, current_char, code_line)
        
    ## Checking for number
    elif (next_char.isdigit()):
        current_char = next_char
        next_char = code_file.read(1)

        while (next_char.isdigit()):
            current_char += next_char
            next_char = code_file.read(1)
            
        code_file.seek(code_file.tell() - 1)
        
        if (next_char.isalpha()):
            print("Syntax error in line " + str(code_line) + ": Letter \"" + next_char + "\" found after digits \"" + current_char)
            sys.exit(0)
        
        if (int(current_char) > 32767):
            print("Syntax error in line " + str(code_line) + ": The given number \"" + current_char + "\" is out of bounds, accepted numbers [-32767, 32767]")
            sys.exit(0)
        
        else:
            token_type = "NUMBER"
            return (token_type, current_char, code_line)

    ## Checking for parentheses
    elif (next_char == '(' or next_char == ')'):
        current_char = next_char
        token_type = "GROUP"
        return (token_type, current_char, code_line)
    
    ## Checking for operator
    elif (next_char == '+' or next_char == '-' or next_char == "*" or next_char == "%"):
        current_char = next_char
        token_type = "OPERATOR"
        return (token_type, current_char, code_line)
 
    ## Checking for division operator
    elif (next_char == '/'):
        current_char = next_char
        next_char = code_file.read(1)

        if (next_char == '/'):
            current_char += next_char
            token_type = "OPERATOR"
            return (token_type, current_char, code_line)
            
        else:
            print("Syntax error in line " + str(code_line) + ": Not recognizing the value \"" + current_char + "\"")
            sys.exit(0)
   
    ## Checking for seperator
    elif (next_char == ':' or next_char == ','):
        current_char = next_char
        token_type = "SEPERATOR"
        return (token_type, current_char, code_line)
    
    ## Checking for correlation or assigmnent
    elif (next_char == '='):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == '='):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            code_file.seek(code_file.tell() - 1)
            token_type = "ASSIGNMENT"
            return (token_type, current_char, code_line)
    
    ## Checking for number correlation
    elif (next_char == '<'):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == '='):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            code_file.seek(code_file.tell() - 1)
            token_type = "ASSIGNMENT"
            return (token_type, current_char, code_line)

    ## Checking for number correlation
    elif (next_char == '>'):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == '='):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            code_file.seek(code_file.tell() - 1)
            token_type = "ASSIGNMENT"
            return (token_type, current_char, code_line)

    ## Checking for number correlation
    elif (next_char == '!'):
        current_char = next_char
        next_char = code_file.read(1)
        
        if (next_char == '='):
            current_char += next_char
            token_type = "CORRELATION"
            return (token_type, current_char, code_line)
        else:
            print("Syntax error in line " + str(code_line) + ": Invalid character after the character \"" + current_char + "\"")
            sys.exit(0)

    ## Print error message if there is invalid syntax
    else:
        current_char = next_char
        print("Syntax error in line " + str(code_line) + ": Invalid syntax \"" + current_char + "\"")
        sys.exit(0)

## Return next token
def next_token():
    global token_index
    token_index += 1
    return (tokens[token_index])

## The main function for all processes
def startCompiling():
    while (not eof_flag):
        lexicalResult = lexicalAnalyzer()
        new_token = Token(lexicalResult[1], lexicalResult[0], lexicalResult[2])
        tokens.append(new_token)
        
    token = next_token()
    while (token.token_type != "EOF"):
        print(token)
        token = next_token()
        
### Main Program
if __name__ == "__main__":
    
    code_line = 1
    eof_flag = False
    token_index = -1
    token = ()
    tokens = []
    keywords = ("main", "def", "#def", "#int", "global", "if",
                "elif", "else", "while", "print", "return",
                "input", "int", "and", "or", "not")
    

    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()

    while lines and lines[-1].strip() == '':
        lines.pop()

    with open(sys.argv[1], 'w') as file:
        file.writelines(lines)
    
    file.close()
    
    code_file = open(sys.argv[1], "r")
    print("Start Compiling...")
    startCompiling()
    print("Compilation Completed succesfully!")
    code_file.close()