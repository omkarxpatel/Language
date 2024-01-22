import re, os, sys, time

class Lexer():
    def __init__(self):
        self.tokens = []
        self.currentPosition = 0
        self.execution = 0
        
        self.patterns = {
            r'\s+': 'WHITESPACE',
            r'\n': 'NEWLINE',
            
            r'\d+': 'NUMBER',
            r'[a-z]+': 'LETTER',
            
            r'\+': 'PLUS',
            r'\-': 'SUBTRACT',
            r'\*': 'MULTIPLY',
            r'\/': 'DIVIDE',
            r'\(': 'OPENPARENTHESIS',
            r'\)': 'CLOSEPARENTHESIS',
            
            r'\for': 'LOOP',
        }
        
        self.charToRegex = {
            '0123456789': r'\d+',
            'abcdefghijklmnopqrstuvwxyz': r'[a-z]+',
        }
        
        self.lookup = {}

    def setupPatterns(self):
        self.execution = time.time()
        for characters, regex in self.charToRegex.items():
            for character in characters:
                self.lookup[character] = regex
                
        for character in "+-*/":
            val = rf'\{character}'
            self.lookup[character] = val
            
        self.lookup["\n"] = r'\n'
        self.lookup["for"] = r'\for'
        self.lookup["("] = r'\('
        self.lookup[")"] = r'\)'
        
    
    def tokenizer(self, value):
        self.setupPatterns()
        operations = 0

        while (self.currentPosition < len(value)):
            character = value[self.currentPosition]
            pattern = self.lookup[character]
            tokenType = self.patterns[pattern]

            regex = re.compile(pattern)
            match = regex.match(value, self.currentPosition)
            spaces = (4 - len(str(self.currentPosition))) * " "

            print(f"{self.currentPosition}{spaces}|  {match} ({tokenType})")
            if not match:
                raise ValueError(f"Invalid token at position {self.currentPosition}")

            self.tokens.append((f"Value: {match.group(0)}", tokenType))
            self.currentPosition = match.end()

            operations += 1

        return operations        
        
    def evaluate_expression(self):
        stack = []
        operations = {
            'PLUS': '+',
            'SUBTRACT': '-',
            'MULTIPLY': '*',
            'DIVIDE': '/',
            'OPENPARENTHESIS': '(',
            'CLOSEPARENTHESIS': ')',
        }
        
        for token, token_type in self.tokens:
            if token_type == 'NUMBER':
                stack.append(int(token.split(":")[1].strip()))
                
            elif token_type in operations.keys():
                stack.append(token_type)
        
        evaluation = ""
        for item in stack:
            if item in operations.keys():
                evaluation += operations.get(item)
            else:
                evaluation += str(item)

        return [stack, eval(evaluation)]

    def main(self, value, output):
        os.system('clear')
        result = self.tokenizer(value)
        calculated_output = self.evaluate_expression()

        spacer = "-"
        # output = self.evaluate_expression()
        print(f"{50*spacer}\nInput: {value}\nOutput: {calculated_output[-1]}\nLiteral: {calculated_output[0]}\n")        
        
        print(f"Execution time: {round(time.time()-self.execution, 5)}s\nOperations: {result}\n\n{self.tokens}")
    
        
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
            Lexer().main(expression, True)
            
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        sys.exit(1)
