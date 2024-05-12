## Nestor Moulias, 4737
## Panagiotis Trypos, 5131

import sys

keywords = ("main", "def", "#def", "#int", "global", "if", "elif", "else", "while", "print", "return", "input", "int", "and", "or", "not")
separators = (":", ",")
operations = ("//", "+", "*", "-", "%")
correlations = ("<", "<=", ">", ">=", "==", "!=")
assignment = ("=")
blocks = ("(", ")", "#{", "#}")

## Lexical Analyzer 
def lexicalAnalyzer(input_text):
    recognized_tokens = []
    tokens = []
    i = 0
    line_number = 1

    while i < len(input_text):
        if input_text[i] == ' ' or input_text[i] == '\t':
            # Ignore whitespaces
            i += 1
        elif input_text[i] == '\n':
            # Increment line number
            line_number += 1
            i += 1
        elif input_text[i:i+2] == '##':
            # Ignore comments
            i += 2
            while input_text[i:i+2] != '##':
                i += 1
            i += 2
        elif input_text[i:i+2] in operations:
            # Check for two-character operations
            recognized_tokens.append(('OPERATOR', input_text[i:i+2], line_number))
            i += 2
        elif input_text[i:i+2] in correlations:
            # Check for two-character correlations
            recognized_tokens.append(('CORRELATION', input_text[i:i+2], line_number))
            i += 2
        elif input_text[i:i+2] in blocks:
            # Check for two-character blocks
            recognized_tokens.append(('BLOCK', input_text[i:i+2], line_number))
            i += 2
        elif input_text[i] in operations:
            # Check for one-character operations
            recognized_tokens.append(('OPERATOR', input_text[i], line_number))
            i += 1
        elif input_text[i] in correlations:
            # Check for one-character correlations
            recognized_tokens.append(('CORRELATION', input_text[i], line_number))
            i += 1
        elif input_text[i] in blocks:
            # Check for one-character blocks
            recognized_tokens.append(('BLOCK', input_text[i], line_number))
            i += 1
        elif input_text[i] in separators:
            # Check for one-character separators
            recognized_tokens.append(('SEPARATOR', input_text[i], line_number))
            i += 1
        elif input_text[i] in assignment:
            # Check for assignment
            recognized_tokens.append(('ASSIGNMENT', input_text[i], line_number))
            i += 1
        else:
            # Identify keywords, identifiers, or integers
            token = ''
            while i < len(input_text) and input_text[i] not in (' ', '\n', '\t') and input_text[i] not in operations and input_text[i:i+2] not in operations and input_text[i] not in correlations and input_text[i:i+2] not in correlations and input_text[i:i+1] not in blocks and input_text[i] not in separators and input_text[i] not in assignment:
                token += input_text[i]
                i += 1
            if token.isdigit():
                recognized_tokens.append(('NUMBER', token, line_number))
            elif token in keywords:
                recognized_tokens.append(('KEYWORD', token, line_number))
            else:
                recognized_tokens.append(('IDENTIFIER', token, line_number))
    
    for token in recognized_tokens:
        new_token = Token(token[1], token[0], token[2])
        tokens.append(new_token)
    return tokens

class Token:
    def __init__(self, recognized_token, token_type, line_number):
        self.recognized_token = recognized_token
        self.token_type = token_type
        self.line_number = line_number
    
    def __str__(self):
        return(self.recognized_token + "\t family: " + self.token_type + "\t Line: " + str(self.line_number))

class Quad:

    def __init__(self, label, operation, argument1, argument2, result):
        self.label = label
        self.operation = operation
        self.argument1 = argument1
        self.argument2 = argument2
        self.result = result

    def __str__(self):
        return str(self.operation) + " " + str(self.argument1) + " " + str(self.argument2) + " " + str(self.result)

class Variable:
    def __init__(self, name, datatype, offset):
        self.name = name
        self.datatype = datatype
        self.offset = offset

    def __str__(self):
        return str(self.name) + " " + str(self.datatype) + " " + str(self.offset)
    
class TemporaryVariable:
    def __init__(self, name, datatype, offset):
        self.name = name
        self.datatype = datatype
        self.offset = offset

    def __str__(self):
        return str(self.name) + " " + str(self.datatype) + " " + str(self.offset)
    
class FormalParameter:
    def __init__(self, name, datatype, offset):
        self.name = name
        self.datatype = datatype
        self.offset = offset

    def __str__(self):
        return str(self.name) + " " + str(self.datatype) + " " + str(self.offset)
    
class Parameter:
    def __init__(self, name, datatype, mode, offset):
        self.name = name
        self.datatype = datatype
        self.mode = mode
        self.offset = offset

    def __str__(self):
        return str(self.name) + " " + str(self.datatype) + " " + str(self.mode) + " " + str(self.offset)
    
class Function:
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype
        self.startingQuad = ""
        self.frameLength = ""
        self.formalParameters = []

    def __str__(self):
        return str(self.name) + " " + str(self.datatype) + " " + str(self.frameLength) + " (" + ", ".join([formalParameter.__str__() for formalParameter in self.formalParameters]) + ")"

    def setStartingQuad(self, quad):
        self.startingQuad = quad
        
    def setFrameLength(self, length):
        self.frameLength = length
        
    def addFormalParameter(self, param):
        self.formalParameters.append(param)

class Scope:
    
    def __init__(self, name, nestingLevel):
        self.name = name
        self.nestingLevel = nestingLevel
        self.entities = []
        self.offset = 12

    def __str__(self):
        return ("(" + str(self.nestingLevel) + "):\t" + "\n\t".join([entity.__str__() for entity in self.entities]))

    def getSize(self):
        return self.offset
    
    def addVariable(self, name):
        self.entities.append(Variable(name, "int", self.offset))
        self.offset += 4

    def addTemporaryVariable(self, name):
        self.entities.append(TemporaryVariable(name, "int", self.offset))
    
    def addFunction(self, name, datatype):
        self.entities.append(Function(name, datatype))

    def addFormalParameter(self, formalParameter):
        self.entities[-1].addFormalParameter(formalParameter)

    def getLastFormalParameter(self):
        return self.entities[-1]
    
    def addParameter(self, name, datatype, mode):
        self.entities.append(Parameter(name, datatype, mode, self.offset))
        self.offset += 4

    def setStartingQuad(self, quad):
        self.entities[-1].setStartingQuad(quad)

    def setFrameLength(self, frameLength):
        self.entities[-1].setFrameLength(frameLength)

class SymbolsTable:
    
    def __init__(self):
        self.scopes = []
        self.scopeStrings = []
        self.mainFrameLength = 0
    
    def getTopScopeSize(self):
        return self.scopes[-1].getSize()
    
    def addScope(self, scopeName):
        self.scopes.append(Scope(scopeName, len(self.scopes)))
        
    def removeLastScope(self):
        self.scopes.pop()
        
    def addFunction(self, name, datatype):
        self.scopes[-1].addFunction(name, datatype)        
    
    def addParameter(self, name, datatype, mode):
        self.scopes[-1].addParameter(name, datatype, mode)
        
    def addVariable(self, name):
        self.scopes[-1].addVariable(name)
        
    def addTemporaryVariable(self, name):
        self.scopes[-1].addTemporaryVariable(name)
        
    def appendFormalParameterToCaller(self):
        self.scopes[-2].addFormalParameter(self.scopes[-1].getLastFormalParameter())
        
    def setStartingQuad(self, quad):
        if (len(self.scopes) == 1):
            return
        self.scopes[-2].setStartingQuad(quad)
        
    def setFrameLength(self, frameLength):
        self.scopes[-1].setFrameLength(frameLength)
        
    def setMainFrameLength(self, frameLength):
        self.mainFrameLength = frameLength
    
    def saveScopeString(self):
        self.scopeStrings.append(self.scopes[-1].__str__())
    
    def saveToFile(self, filename):
        with open(filename + ".sym", "w") as file:
            for scope in self.scopeStrings:
                file.write(scope + "\n\n")

    def printScopeTrace(self):
        for scope in self.scopeStrings:
            print(scope + "\n")

class IntermediateCode:

    def __init__(self):
        self.quadList = []
        self.label = 100
        self.variableCount = 0

    def genQuad(self, operation, argument1, argument2, result):
        quad = Quad(str(self.label), operation, argument1, argument2, result)
        self.quadList.append(quad)
        self.label += 1
        return quad
    
    def nextQuad(self):
        return str(self.label)
    
    def newTemp(self):
        self.variableCount += 1
        return "T_" + str(self.variableCount)
    
    def emptyList(self):
        return []
    
    def makeList(self, label):
        return [label]
    
    def mergeList(self, list1, list2):
        return list1 + list2
    
    def backpatch(self, list, label):
        for item in list:
            self.quadList[int(item)-100].result = label
        return
    
    def saveToFile(self, filename):
        with open(filename + ".int", "w") as file:
            for quad in self.quadList:
                file.write(quad.__str__() + "\n")
    
    def printOut(self):
        for quad in self.quadList:
            print(quad.__str__())

class SyntaxAnalyzer:

    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.token = None
        self.intermediateCode = IntermediateCode()
        self.symbolsTable = SymbolsTable()

    ## Return next token
    def nextToken(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.token = tokens[self.token_index]
        else:
            # If there are no more tokens, return a special token indicating end of file (EOF)
            self.token = Token("EOF", "EOF", -1)

    ## Return previous token
    def previousToken(self):
        self.token_index -= 1
        if self.token_index > -1:
            self.token = self.tokens[self.token_index]

    ## Check the syntax of global statement
    def globalStatement(self):
        while (self.token.recognized_token == "global"):
            self.nextToken()
            if (self.token.token_type == "IDENTIFIER"):
                self.nextToken()
                while (self.token.recognized_token == ","):
                    self.nextToken()
                    if (self.token.token_type == "IDENTIFIER"):
                        self.nextToken()
                    else:
                        print("Syntax error in line " + str(self.token.line_number) + ": IDENTIFIER expected, but " + self.token.token_type + " " + self.token.recognized_token + " recieved.")
                        sys.exit(0)
            else:
                print("Syntax error in line " + str(self.token.line_number) + ": IDENTIFIER expected, but " + self.token.token_type + " " + self.token.recognized_token + " recieved.")
                sys.exit(0)
        
    ## Check if the definition of variables is correct
    def defineVariables(self):
        check_line = self.token.line_number
        if (self.token.token_type == "IDENTIFIER"):
            self.symbolsTable.addVariable(self.token.recognized_token)
            self.nextToken()
            while (self.token.recognized_token == ","):
                self.nextToken()
                if (self.token.token_type == "IDENTIFIER"):
                    self.symbolsTable.addVariable(self.token.recognized_token)
                    self.nextToken()
                else:
                    print("Syntax error in line " + str(check_line) + ": IDENTIFIER expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
                    sys.exit(0)
        else:
            print("Syntax error in line " + str(check_line) + ": IDENTIFIER expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
            sys.exit(0)

    def intStatement(self):
        if (self.token.recognized_token == "int"):
            self.nextToken()
            if (self.token.recognized_token == "("):
                self.nextToken()
                if (self.token.recognized_token == "input"):
                    self.nextToken()
                    if (self.token.recognized_token == "("):
                        self.nextToken()
                        if (self.token.recognized_token == ")"):
                            self.nextToken()
                            if (self.token.recognized_token == ")"):
                                self.nextToken()
                            else:
                                print("Syntax error in line " + str(self.token.line_number-1) + ": \")\" expected, but " + self.token.token_type + " recieved.")
                                sys.exit(0)
                        else:
                            print("Syntax error in line " + str(self.token.line_number-1) + ": \")\" expected, but " + self.token.token_type + " recieved.")
                            sys.exit(0)
                    else:
                        print("Syntax error in line " + str(self.token.line_number) + ": \"(\" expected, but " + self.token.token_type + " recieved.")
                        sys.exit(0)
                else:
                    print("Syntax error in line " + str(self.token.line_number) + ": \"input\" expected, but " + self.token.token_type + " recieved.")
                    sys.exit(0)
            else:
                print("Syntax error in line " + str(self.token.line_number) + ": \"(\" expected, but " + self.token.recognized_token + " recieved.")
                sys.exit(0)

    def assignmentStatement(self, variableName):
        check_line = self.token.line_number
        self.nextToken()
        if (self.token.recognized_token == "="):
            self.nextToken()
            if (self.token.recognized_token == "int"):
                self.intStatement()
            elif (check_line == self.token.line_number):
                E_place = self.expression()
                self.intermediateCode.genQuad("=", E_place, "_", variableName)
        else:
            print("Syntax error in line " + str(self.token.line_number) + ": Invalid syntax, \"" + self.token.recognized_token + "\" not expected.")
            sys.exit(0)

    def functionParameters(self):
        parameters = []
        parameter = self.expression()
        parameters.append(parameter)

        while (self.token.recognized_token == ","):
            self.nextToken()
            parameter = self.expression()
            parameters.append(parameter)

        for i in parameters:
            self.intermediateCode.genQuad("par", i, "CV", "_")

    def checkIdentifier(self):
        if (self.token.token_type == "IDENTIFIER"):
            identifier = self.token.recognized_token
            self.nextToken()
            if (self.token.recognized_token == "("):
                self.nextToken()
                self.functionParameters()

                w = self.intermediateCode.newTemp()
                self.intermediateCode.genQuad("par", w, "RET", "_")
                self.intermediateCode.genQuad("call", identifier, "_", "_")

                self.symbolsTable.addTemporaryVariable(w)

                if (self.token.recognized_token == ")"):
                    self.nextToken()
                else:
                    print("Syntax error in line " + str(self.token.line_number) + ": \")\" expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
                    sys.exit(0)
                
                return w
            
            return identifier

    def condition(self):
        B_true, B_false = self.boolTerm()

        while (self.token.recognized_token == "or"):
            self.intermediateCode.backpatch(B_false, self.intermediateCode.nextQuad())
            self.nextToken()

            Q2_true, Q2_false = self.boolTerm()
            B_true = self.intermediateCode.mergeList(B_true, Q2_true)
            B_false = Q2_false

        return B_true, B_false
    
    def boolTerm(self):
        Q_true, Q_false = self.boolFactor()

        while (self.token.recognized_token == "and"):
            self.intermediateCode.backpatch(Q_true, self.intermediateCode.nextQuad())

            self.nextToken()
            R2_true, R2_false = self.boolFactor()
            Q_false = self.intermediateCode.mergeList(Q_false, R2_false)
            Q_true = R2_true
        
        return Q_true, Q_false

    def boolFactor(self):
        if (self.token.recognized_token == "not"):
            self.nextToken()

            if (self.token.recognized_token == "("):
                self.nextToken()
                B_true, B_false = self.condition()

                if (self.token.recognized_token == ")"):
                    self.nextToken()
                else:
                    print("Syntax error in line " + str(self.token.line_number) + ": \")\" expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
                    sys.exit(0)

                return B_false, B_true
            
            else:
                print("Syntax error in line " + str(self.token.line_number) + ": \"(\" expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
                sys.exit(0)
        
        elif (self.token.recognized_token == "("):
            self.nextToken()
            B_true, B_false = self.condition()

            if (self.token.recognized_token == ")"):
                self.nextToken()
            else:
                print("Syntax error in line " + str(self.token.line_number) + ": \")\" expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
                sys.exit(0)

            return B_true, B_false 
        
        else:
            E1_place = self.expression()

            if (self.token.recognized_token in correlations):
                correlation = self.token.recognized_token
                self.nextToken()
            else:
                print("Syntax error in line " + str(self.token.line_number) + ": CORRELATION expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
                sys.exit(0)
            
            E2_place = self.expression()
            R_true = self.intermediateCode.makeList(self.intermediateCode.nextQuad())
            self.intermediateCode.genQuad(correlation, E1_place, E2_place, "_")
            R_false = self.intermediateCode.makeList(self.intermediateCode.nextQuad())
            self.intermediateCode.genQuad("jump", "_", "_", "_")
            return R_true, R_false

    ## Check if an expression is starting with + or - sign
    def optionalSign(self):
        if(self.token.recognized_token == "+" or self.token.recognized_token == "-"):
            sign = self.token.recognized_token
            self.nextToken()
            return sign
        else:
            return ""

    def factor(self):
        if (self.token.token_type == "NUMBER"):
            factor = self.token.recognized_token
            self.nextToken()
            return factor
        elif (self.token.recognized_token == "("):
            self.nextToken()
            factor = self.expression()
            if (self.token.recognized_token == ")"):
                self.nextToken()
            else:
                print("Syntax error in line " + str(self.token.line_number) + ": \")\" expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
                sys.exit(0)
            return factor
        elif (self.token.token_type == "IDENTIFIER"):
            factor = self.checkIdentifier()
            return factor
        else:
            print("Syntax error in line " + str(self.token.line_number) + ": Invalid expression.")
            sys.exit(0)

    def term(self):
        F1_place = self.factor()
        
        while (self.token.recognized_token == "*" or self.token.recognized_token == "//" or self.token.recognized_token == "%"):
            operation = self.token.recognized_token
            self.nextToken()
            F2_place = self.factor()
            w = self.intermediateCode.newTemp()
            self.intermediateCode.genQuad(operation, F1_place, F2_place, w)
            F1_place = w

            self.symbolsTable.addTemporaryVariable(w)

        return F1_place

    def expression(self):
        T1_place = self.optionalSign() + self.term()

        while (self.token.recognized_token == "+" or self.token.recognized_token == "-"):
            operation = self.token.recognized_token
            self.nextToken()
            T2_place = self.term()
            w = self.intermediateCode.newTemp()
            self.intermediateCode.genQuad(operation, T1_place, T2_place, w)
            T1_place = w
            
            self.symbolsTable.addTemporaryVariable(w)

        return T1_place

    def elseStatement(self):
        if (self.token.recognized_token == "else"):
            self.nextToken()
            if (self.token.recognized_token == ":"):
                self.nextToken()
                if (self.token.recognized_token == "#{"):
                    self.nextToken()
                    self.codeBlock()
                else:
                    self.statement()
            else:
                print("Syntax error in line " + str(self.token.line_number) + ": SEPERATOR \":\" expected, but " + self.token.token_type + " " + self.token.recognized_token + " recieved.")
                sys.exit(0)


    def elifStatement(self):
        while (self.token.recognized_token == "elif"):
            self.nextToken()
            condition_true, condition_false = self.condition()
            if (self.token.recognized_token == ":"):
                self.nextToken()
                if (self.token.recognized_token == "#{"):
                    self.nextToken()
                    self.intermediateCode.backpatch(condition_true, self.intermediateCode.nextQuad())
                    
                    self.codeBlock()
                    
                    ifList = self.intermediateCode.makeList(self.intermediateCode.nextQuad())
                    self.intermediateCode.genQuad("jump", "_", "_", "_")
                    self.intermediateCode.backpatch(condition_false, self.intermediateCode.nextQuad())
                    self.codeBlock()
                else:
                    self.intermediateCode.backpatch(condition_true, self.intermediateCode.nextQuad())
                    self.statement()
                    ifList = self.intermediateCode.makeList(self.intermediateCode.nextQuad())
                    self.intermediateCode.genQuad("jump", "_", "_", "_")
                    self.intermediateCode.backpatch(condition_false, self.intermediateCode.nextQuad())
                    self.elifStatement()
                    self.elseStatement()
                    self.intermediateCode.backpatch(ifList, self.intermediateCode.nextQuad())
            else:
                print("Syntax error in line " + str(self.token.line_number) + ": SEPERATOR \":\" expected, but " + self.token.recognized_token + " recieved.")
                sys.exit(0)

    def ifStatement(self):
        condition_true, condition_false = self.condition()
        if (self.token.recognized_token == ":"):
            self.nextToken()
            if (self.token.recognized_token == "#{"):
                self.nextToken()
                self.intermediateCode.backpatch(condition_true, self.intermediateCode.nextQuad())
                
                self.codeBlock()

                ifList = self.intermediateCode.makeList(self.intermediateCode.nextQuad())
                self.intermediateCode.genQuad("jump", "_", "_", "_")
                self.intermediateCode.backpatch(condition_false, self.intermediateCode.nextQuad())
                self.elifStatement()
                self.elseStatement()
                self.intermediateCode.backpatch(ifList, self.intermediateCode.nextQuad())
            else:
                self.intermediateCode.backpatch(condition_true, self.intermediateCode.nextQuad())
                self.statement()
                ifList = self.intermediateCode.makeList(self.intermediateCode.nextQuad())
                self.intermediateCode.genQuad("jump", "_", "_", "_")
                self.intermediateCode.backpatch(condition_false, self.intermediateCode.nextQuad())
                self.elifStatement()
                self.elseStatement()
                self.intermediateCode.backpatch(ifList, self.intermediateCode.nextQuad())
        else:
            print("Syntax error in line " + str(self.token.line_number) + ": SEPERATOR \":\" expected, but " + self.token.recognized_token + " recieved.")
            sys.exit(0)

    def whileStatement(self):
        conditionQuad = self.intermediateCode.nextQuad()
        condition_true, condition_false = self.condition()
        if (self.token.recognized_token == ":"):
            self.nextToken()
            if (self.token.recognized_token == "#{"):
                self.nextToken()
                self.intermediateCode.backpatch(condition_true, self.intermediateCode.nextQuad())
                self.codeBlock()
                self.intermediateCode.genQuad("jump", "_", "_", conditionQuad)
                self.intermediateCode.backpatch(condition_false, self.intermediateCode.nextQuad())
            else:
                self.intermediateCode.backpatch(condition_true, self.intermediateCode.nextQuad())
                self.statement()
                self.intermediateCode.genQuad("jump", "_", "_", conditionQuad)
                self.intermediateCode.backpatch(condition_false, self.intermediateCode.nextQuad())
        else:
            print("Syntax error in line " + str(self.token.line_number) + ": SEPERATOR \":\" expected, but " + self.token.token_type + " " + self.token.recognized_token + " recieved.")
            sys.exit(0)

    def printStatement(self):
        if (self.token.recognized_token == "("):
            self.nextToken()
            E_place = self.expression()
            self.intermediateCode.genQuad("out", E_place, "_", "_")
            if (self.token.recognized_token == ")"):
                self.nextToken()
            else:
                print("Syntax error in line " + str(self.token.line_number) + ": \")\" expected, but \"" + self.token.recognized_token + "\" recieved.")
                sys.exit(0)
        else:
            print("Syntax error in line " + str(self.token.line_number) + ": \"(\" expected, but " + self.token.recognized_token + " recieved.")
            sys.exit(0)

    ## Check the syntax of return statement
    def returnStatement(self):
        check_line = self.token.line_number
        self.nextToken()
        if(check_line != self.token.line_number):
            return
        E_place = self.expression()
        self.intermediateCode.genQuad("ret", "_", "_", E_place)

    def statement(self):
        if (self.token.token_type == "IDENTIFIER"):
            variableName = self.token.recognized_token
            self.assignmentStatement(variableName)
        if (self.token.recognized_token == "if"):
            self.nextToken()
            self.ifStatement()
        elif (self.token.recognized_token == "while"):
            self.nextToken()
            self.whileStatement()
        elif (self.token.recognized_token == "print"):
            self.nextToken()
            self.printStatement()
        elif (self.token.recognized_token == "return"):
            self.returnStatement()
    
    def codeBlock(self):
        while (self.token.recognized_token != "#}"):
            self.statement()
        self.nextToken()

    ## Check if there are declarations
    def declarations(self):
        while (self.token.recognized_token == "#int"):
            self.nextToken()
            self.defineVariables()

    ## Check if the definition of parameters is correct
    def defineParameters(self):
        check_line = self.token.line_number
        if (self.token.token_type == "IDENTIFIER"):

            parameterName = self.token.recognized_token
            self.symbolsTable.addParameter(parameterName, "int", "cv")
            self.symbolsTable.appendFormalParameterToCaller()

            self.nextToken()
            while (self.token.recognized_token == ","):
                self.nextToken()
                if (self.token.token_type == "IDENTIFIER"):

                    parameterName = self.token.recognized_token
                    self.symbolsTable.addParameter(parameterName, "int", "cv")
                    self.symbolsTable.appendFormalParameterToCaller()

                    self.nextToken()
                else:
                    print("Syntax error in line " + str(check_line) + ": IDENTIFIER expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
                    sys.exit(0)

    ## Check if the definition of functions is correct
    def function(self):
        if (self.token.token_type == "IDENTIFIER"):
            self.nextToken()
            if (self.token.recognized_token == "("):
                self.nextToken()
                self.defineParameters()
                if (self.token.recognized_token == ")"):
                    self.nextToken()
                    if (self.token.recognized_token == ":"):
                        self.nextToken()
                        if (self.token.recognized_token == "#{"):
                            self.nextToken()
                            self.declarations()
                            self.functions()
                            self.globalStatement()
                            self.codeBlock()
                        else:
                            print("Syntax error in line " + str(self.token.line_number) + ": #{ expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
                            sys.exit(0)
                    else:
                        print("Syntax error in line " + str(self.token.line_number) + ": SEPERATOR \":\" expected, but " + self.token.recognized_token + " recieved.")
                        sys.exit(0)
                else:
                    print("Syntax error in line " + str(self.token.line_number) + ": \")\" expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
                    sys.exit(0)
            else:
                print("Syntax error in line " + str(self.token.line_number) + ": \"(\" expected, but " + self.token.token_type + " \"" + self.token.recognized_token + "\" recieved.")
                sys.exit(0)
        else:
            print("Syntax error in line " + str(self.token.line_number) + ": IDENTIFIER expected, but \"" + self.token.token_type + "\" recieved.")
            sys.exit(0)

    ## Check if there are functions
    def functions(self):
        while (self.token.recognized_token == "def"):
            self.nextToken()

            functionName = self.token.recognized_token
            self.symbolsTable.addFunction(functionName, "int")
            self.symbolsTable.addScope(functionName)

            self.function()

            frameLength = self.symbolsTable.getTopScopeSize()
            self.symbolsTable.saveScopeString()
            self.symbolsTable.removeLastScope()
            self.symbolsTable.setFrameLength(frameLength)

    ## Check if the definition of main program and the format of it is correct
    def mainProgram(self):

        self.symbolsTable.setStartingQuad(self.intermediateCode.nextQuad())

        check_line = self.token.line_number
        self.nextToken()
        if (self.token.recognized_token == "main"):
            self.nextToken()
            self.declarations()
            while (self.token.recognized_token != "EOF"):
                self.statement()
                self.nextToken
        else:
            print("Syntax error in line " + str(check_line) + ": The definition of main program is incorrect")
            sys.exit(0)

    ## Define the main format of the program
    def program(self, filename):
        self.nextToken()

        self.symbolsTable.addScope("main")

        self.declarations()
        self.functions()
        check_line = self.token.line_number

        if (self.token.recognized_token != "#def"):
            print("Syntax error in line " + str(check_line) + ": Unexpected token \"" + self.token.recognized_token + "\" recieved, You should define the main part of program.")
            sys.exit(0)
        
        self.intermediateCode.genQuad("begin_block", "main", "_", "_")

        self.mainProgram()

        self.intermediateCode.genQuad("halt", "_", "_", "_")
        self.intermediateCode.genQuad("end_block", "main", "_", "_")

        frameLength = self.symbolsTable.getTopScopeSize()
        self.symbolsTable.saveScopeString()
        self.symbolsTable.removeLastScope()
        self.symbolsTable.setMainFrameLength(frameLength)

        print("====================")
        print("Saving intermediate code to file \"" + filename + ".int\"...")
        self.intermediateCode.saveToFile(filename)
        print("Saving completed.")
        print("\nSaving symbols table to file \"" + filename + ".sym\"...")
        self.symbolsTable.saveToFile(filename)
        print("Saving completed.")
        print("====================")

### Main Program
def compiler(code, filename):
    print("Start of the compilation process...")
    
    global tokens
    tokens = lexicalAnalyzer(code)
    syntax_analyzer = SyntaxAnalyzer(tokens)
    syntax_analyzer.program(filename)

    print("Compilation process completed successfully!")

def main():
    if len(sys.argv) != 2:
        print("Usage: python compiler.py [filename]")
        return   

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            filename = filename[:-4]
            input_code = file.read()
            compiler(input_code, filename)
    except FileNotFoundError:
        print("Error: File not found")

### Main Program
if __name__ == "__main__":
    main()
