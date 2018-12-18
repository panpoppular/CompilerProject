import string as s
import sys

# File scanner
lines = []
inputFile = open(sys.argv[1],"r")
outputFile = open(sys.argv[2],"w")
for line in inputFile :
    lines.append(line.strip().split())

varName = set()

# Grammar checking

def isID(val) :
    if val.isupper() and len(val)==1 :
        return True
    return False

def isCONST(val) :
    if val.isdigit() :
        if 0 <= int(val) <= 100: return True
    return False

def isTerm(val) :
    return isID(val) or isCONST(val)

def isExpOP(val) :
    return val=="+" or val=="-"

def isCondOP(val) :
    return val=="<" or val=="="

def isEXP(list) :
    if len(list)==1 :
        return isTerm(list[0])
    return isTerm(list[0]) and isTerm(list[2]) and isExpOP(list[1])

def isLineNum(val):
    if val.isdigit():
        if 1<=int(val)<=1000 :
            return True
    return False

def checkIF(line) :
        if len(line) > 6 : raise()
        if not (isTerm(line[2]) and isTerm(line[4]) ) :
            raise()
        if not isCondOP(line[3]) :
            raise()
        if not isLineNum(line[5]) :
            raise()

def checkStatement(line,ptr) :
    #print(line)
    if not isLineNum(line[0]) : raise()
    if line[1] == "IF" :
        checkIF(line)
    elif line[1] == "GOTO" :
        if len(line) > 3 or not isLineNum(line[2]) :
            raise()
    elif line[1] == "PRINT" :
        if len(line) > 3 or not isID(line[2]) :
            raise()
    elif line[1] == "STOP" :
        if len(line) > 2 : raise()
        return True
    else :
        if line[2] != "=": raise ()
        if len(line) == 4 or len(line) == 6 :
            if not(isEXP(line[3:len(line)]) ) :
                raise()
            if not isID(line[1]) : raise()
        else :
            raise()
    return False

# Code generation converter
def valueID(char) :
    return str(ord(char) - ord('A') +1)

def parseCond(var) :
    if isID(var):
        return "11 " + valueID(var) + " "
    elif isCONST(var):
        return "12 " + str(var) + " "
    else:
        if var == "+":
            return "17 1 "
        elif var == "-":
            return "17 2 "
        elif var == "<":
            return "17 3 "
        elif var == "=":
            return "17 4 "

def decode(line) :
    bCode = ""
    bCode += "10 "+str(line[0])+" "
    if line[1] == "IF" :
        bCode += "13 0 "
        for i in range(2,5) :
            bCode += parseCond(line[i])
        bCode += "14 "+str(line[5])
    elif line[1] == "GOTO" :
        bCode += "14 "+str(line[2])
    elif line[1] == "PRINT" :
        bCode += "15 0 11 "+valueID(line[2])
    elif line[1] == "STOP" :
        bCode += "16 0"
    else :
        for i in range(1 ,len(line)) :
            bCode += parseCond(line[i])

    return bCode.strip()

# Code generation
isEOF = False
linePointed = 0
try :
    for line in lines :
        linePointed += 10
        if isEOF: raise ()
        isEOF = checkStatement(line, linePointed)
        bCode = decode(line)
        print(bCode)
        outputFile.write(bCode+"\n")
    if isEOF :
        print("0")
        outputFile.write("0")

except : print("Syntax Error in Line "+ str(linePointed) )
inputFile.close()
outputFile.close()
