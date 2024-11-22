class Token:
    def __init__(self, type, lexeme, line=1, column=1):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token: {self.type}, Lexeme: {self.lexeme}"

class SymbolTableEntry:
    def __init__(self, name, type, params=None):
        self.name = name
        self.type = type
        self.params = params or []

class ScriptingLanguageLexer:
    def __init__(self):
        self.keywords = {
            'LET', 'IF', 'THEN', 'ELSE', 'ENDIF', 
            'WHILE', 'DO', 'ENDWHILE', 'FOR', 'TO', 
            'STEP', 'ENDFOR', 'FUNC', 'BEGIN', 
            'END', 'RETURN', 'IN', 'REPEAT', 
            'UNTIL', 'CALL'
        }
        
        self.symbol_table = {}
    
    def tokenize(self, source_code):
        tokens = []
        line = 1
        column = 1
        i = 0
        
        while i < len(source_code):
            # Skip whitespace
            while i < len(source_code) and source_code[i].isspace():
                if source_code[i] == '\n':
                    line += 1
                    column = 1
                i += 1
                if i >= len(source_code):
                    break
            
            if i >= len(source_code):
                break
            
            # Comments
            if source_code[i] == '{':
                while i < len(source_code) and source_code[i] != '}':
                    i += 1
                i += 1
                continue
            
            # Keywords and Identifiers
            if source_code[i].isalpha():
                start = i
                while i < len(source_code) and (source_code[i].isalnum() or source_code[i] == '_'):
                    i += 1
                lexeme = source_code[start:i]
                
                # Determine token type
                if lexeme in self.keywords:
                    token_type = lexeme.lower()
                    tokens.append(Token(token_type, lexeme, line, column))
                else:
                    tokens.append(Token('identifier', lexeme, line, column))
                    # Track in symbol table
                    if lexeme not in self.symbol_table:
                        self.symbol_table[lexeme] = SymbolTableEntry(lexeme, 'integer')
                column += i - start
                continue
            
            # Numbers
            if source_code[i].isdigit():
                start = i
                while i < len(source_code) and source_code[i].isdigit():
                    i += 1
                lexeme = source_code[start:i]
                tokens.append(Token('number', lexeme, line, column))
                column += i - start
                continue
            
            # Relational and Arithmetic Operators
            if source_code[i] in '<>+-*/':
                tokens.append(Token('operator', source_code[i], line, column))
                column += 1
                i += 1
                continue
            
            # Specific token types for special characters
            if source_code[i] == '=':
                tokens.append(Token('equal', source_code[i], line, column))
                column += 1
                i += 1
                continue
            
            if source_code[i] == '(':
                tokens.append(Token('left_paren', source_code[i], line, column))
                column += 1
                i += 1
                continue
            
            if source_code[i] == ')':
                tokens.append(Token('right_paren', source_code[i], line, column))
                column += 1
                i += 1
                continue
            if source_code[i] == '{':
                tokens.append(Token('left_curl_bracket', source_code[i], line, column))
                column += 1
                i += 1
                continue
            if source_code[i] == '}':
                tokens.append(Token('right_curl_bracket', source_code[i], line, column))
                column += 1
                i += 1
                continue
            if source_code[i] == '[':
                tokens.append(Token('left_bracket', source_code[i], line, column))
                column += 1
                i += 1
                continue
            if source_code[i] == ']':
                tokens.append(Token('right_bracket', source_code[i], line, column))
                column += 1
                i += 1
                continue
            
            # Comma
            if source_code[i] == ',':
                tokens.append(Token('comma', source_code[i], line, column))
                column += 1
                i += 1
                continue
            
            # Unexpected character
            i += 1
        
        return tokens
    
    def enhance_symbol_table(self, tokens):
        # Enhance symbol table with function and parameter information
        for i in range(len(tokens)):
            if tokens[i].type == 'call' and i+1 < len(tokens) and tokens[i+1].type == 'identifier':
                func_name = tokens[i+1].lexeme
                # Collect parameters
                if i+2 < len(tokens) and tokens[i+2].type == 'left_paren':
                    params = []
                    j = i+3
                    while j < len(tokens) and tokens[j].type != 'right_paren':
                        if tokens[j].type == 'identifier':
                            params.append(tokens[j].lexeme)
                        j += 1
                    # Update symbol table entry for function
                    self.symbol_table[func_name] = SymbolTableEntry(func_name, 'function (with parameters: ' + ', '.join(params) + ')', params)

def main():
    # Example source code
    source_code = """
LET a = 5
LET b = 10
IF a < b
THEN
LET c = a + b
LET d = c * 2
ELSE
LET e = a - b
ENDIF
CALL myFunction(a, b)
"""
    
    lexer = ScriptingLanguageLexer()
    
    # Tokenize the source code
    tokens = lexer.tokenize(source_code)
    
    # Enhance symbol table
    lexer.enhance_symbol_table(tokens)
    
    # Print Tokens
    print("Tokens:")
    for token in tokens:
        if token.lexeme.strip():  # Skip empty tokens
            print(token)
    
    # Print Symbol Table
    print("\nSymbol Table:")
    for name, entry in lexer.symbol_table.items():
        print(f"Name: {name}, Type: {entry.type}")

if __name__ == "__main__":
    main()