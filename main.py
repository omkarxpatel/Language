import os
import re
import sys
import time
from colorama import Fore as f, init

class Lexer:    
    def __init__(self):
        init(autoreset=True)
        self.execution = time.time()
        
        self.currentPosition = 0

        self.doubleChecking = {
            # comments
            "/": "//"
        }
        self.lookupKeyword = { # .rot syntax
            # reserved words
            "cout": "PRINT",
            "coutln": "PRINTLN",
            # "for": "FOR",
            # "until": "UNTIL",
            
            # quotes
            '\"': r'\"', 
            "\'": r"\'",
            
            # arithmatic operators
            "+": r"\+",
            "-": r"\-",
            "*": r"\*",
            "/": r"\/",
            
            # special symbols
            "(": r"\(",
            ")": r"\)",
            " ": r"\s+",
            "\n": r"\n",
            "=": r"\=",
            "//": r"//",
        }

        self.keywordTypes = { # values to token types
            # reserved words
            r"\d+": "NUMBER",
            r"[a-z]+": "STRING",
            r"[A-Z]+": "STRING",
            "print": "PRINT",
            # "for": "FOR",
            # "until": "UNTIL",
            
            # quotes
            r'\"': "QUOTE",
            r'\'': "SINGLE_QUOTE",
            
            # arithmatic operators
            r"\+": "ADDITION",
            r"\-": "SUBTRACTION",
            r"\*": "MULTIPLICATION",
            r"\/": "DIVISION",
            r"\=": "SETVALUE",
            
            # special symbols
            r"\(": "L_PAREN",
            r"\)": "R_PAREN",
            r"\s+": "SPACE",
            r"\n": "NEWLINE",
            r"//": "COMMENT"
        }
        
        self.antiKeyword = { # token types to python, only requires different syntax
            # reserved words
            "PRINT": "print",
            "PRINTLN": "print*",
            "COMMENT": "# ",
            # "until": " ",
        }
        
        self.tokens = []

    def setupKeywords(self) -> None:
        print("-"*65)
        keywordConfiguration = {
            '0123456789': r'\d+',
            'abcdefghijklmnopqrstuvwxyz': r'[a-z]+',
        }
        self.execution = time.time()
        for characters, regex in keywordConfiguration.items():
            for character in characters:
                self.lookupKeyword[character] = regex
                
        for character in "+-*/":
            val = rf'\{character}'
            self.lookupKeyword[character] = val
            
            
    def tokenizer(self, value) -> int:
        self.setupKeywords()
        operations = 0
        
        while (self.currentPosition < len(value)):
            currentCharacter = value[self.currentPosition]
            
            try:
                identifier = self.lookupKeyword[currentCharacter]
                regex = re.compile(identifier)
                token = regex.match(value, self.currentPosition)

                if not identifier:
                    print("Invalid Identifier at position: ", self.currentPosition)
                    
                try:
                    tokenType = self.keywordTypes[identifier]
                    
                    if tokenType == "STRING":
                        try:
                            tokenType = self.lookupKeyword[token.group(0)] or "STRING"
                        except:
                            pass
                except:
                    tokenType = "UNKNOWN"
                    
                self.currentPosition = token.end()
                self.tokens.append([token.group(0), tokenType])
                
                spaces = " "*(5-len(str(operations)))
                spaces2 = " "*(45-len(str(token)))
                print(f"{operations}{spaces}|  {token}{spaces2}|  {tokenType}")
                
            except:
                print(".",currentCharacter,".")
                self.currentPosition += 1
        
            operations += 1
            
        print("-"*65)
        return operations
    
    
    def parser(self, tokens) -> str:
        self.execution = time.time()
        operations = 0
        backtrack = 0 # used just for println
        idx = 0
        result = ""
        
        print("-"*30)
        for value, tokenType in tokens:
            parsedValue = self.antiKeyword.get(tokenType) or value
            
            if len(parsedValue) != 1:
                if parsedValue == "print": # checks for newline at end
                    openParenthesis = 0
                    
                    for i in range(idx, len(tokens)):
                        token = tokens[i][-1]
                        
                        if token == "L_PAREN":
                            openParenthesis += 1
                        elif token == "R_PAREN":
                            openParenthesis -= 1
                            
                            if openParenthesis == 0:
                                temp = [", end=\"\"", "ENDL"]
                                tokens.insert(i, temp)
                                idx = i+2
                                break
                            
                elif parsedValue == "print*":
                    parsedValue = parsedValue.strip("*")
                
            if parsedValue == "print":
                try:
                    if result[-5:] == "print":
                        pass
                    else:
                        result += parsedValue
                except:
                    pass
            else:
                    checker = self.doubleChecking.get(parsedValue) or None # for double characters like // (comment)
                    if checker:
                        nextToken = tokens[operations-1][0]
                        if (nextToken+parsedValue == checker):
                            # i+=1
                            result += self.antiKeyword.get(self.keywordTypes.get(checker))
                    else:
                        result += parsedValue
                
            operations += 1
            
            if parsedValue == "\n" or tokenType == "SPACE":
                value, parsedValue = repr(value), repr(parsedValue)

                
            spaces = " "*(5-len(str(operations)))
            spaces2 = " "*(10-len(value))

            print(f"{operations}{spaces}|  {value}{spaces2}->    {parsedValue}")
        print("-"*30)
            
        return [result, operations]
    
    
    def save_to_py_file(self, python_code, output_file='output.py'):
        with open(output_file, 'w') as py_file:
            py_file.write(python_code)
        print(f"Saved to {output_file}")    
        
    def main(self, value) -> None:
        os.system('clear')
        print(f"{f.RED}Input File:\n\n{f.RESET}{value}\n\n")
        
        # Compute the source file into tokens
        print(f"{f.RED}Process 1 - Tokenizer:")
        operations = self.tokenizer(value)
        # print(f"Tokens: {self.tokens}")
        print(f"\nExecution time: {round(time.time()-self.execution, 7)}s\nOperations: {operations}")
        
        # Compute the tokens into python code
        print(f"\n\n{f.RED}Process 2 - Parser:")
        evaluation = self.parser(self.tokens)
        self.save_to_py_file(evaluation[0])
        print(f"\nExecution time: {round(time.time()-self.execution, 7)}s\nOperations: {evaluation[1]}")
        
        # Evaluate the python code
        self.execution = time.time()
        print(f"\n\n{f.RED}Process 3 - Execution (output):\n")
        exec(evaluation[0]) # python built in function
        print(f"\nExecution Time: {round(time.time()-self.execution, 7)}")
        
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 interpreter.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    if filename.split(".")[1] != "rot":
        print(f"File {filename} needs to be a .rot file")
        exit(1)
    try:
        with open(filename, 'r') as file:
            expression = file.read()
            Lexer().main(expression)
            
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        sys.exit(1)
