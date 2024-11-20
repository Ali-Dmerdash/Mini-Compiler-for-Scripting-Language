import re

# Reserved Keywords
KEYWORDS = {
    "LET", "IF", "THEN", "ELSE", "ENDIF", "WHILE", "DO", "ENDWHILE",
    "FOR", "TO", "STEP", "IN", "ENDFOR", "REPEAT", "UNTIL", "FUNC",
    "BEGIN", "RETURN", "END", "CALL", "AND", "OR", "NOT"
}

# Token Patterns
TOKEN_PATTERNS = [
    ("keyword", r"\b(?:LET|IF|THEN|ELSE|ENDIF|WHILE|DO|ENDWHILE|FOR|TO|STEP|IN|ENDFOR|REPEAT|UNTIL|FUNC|BEGIN|RETURN|END|CALL|AND|OR|NOT)\b"),
    ("identifier", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("number", r"\b\d+(\.\d+)?\b"),
    ("operator", r"[+\-*/<>!]?=|[+\-*/<>]"),
    ("increment", r"\+\+|--"),
    ("comma", r","),
    ("left_paren", r"\("),
    ("right_paren", r"\)"),
    ("left_bracket", r"\["),
    ("right_bracket", r"\]"),
    ("brace_comment", r"\{[^}]*\}"),
    ("whitespace", r"\s+"),
    ("unknown", r"."),
]

# Compile Patterns
TOKEN_REGEX = [(name, re.compile(pattern)) for name, pattern in TOKEN_PATTERNS]

# Lexical Analyzer Class
class LexicalAnalyzer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.symbol_table = {}

    def tokenize(self):
        position = 0
        while position < len(self.source_code):
            match = None
            for token_name, pattern in TOKEN_REGEX:
                match = pattern.match(self.source_code, position)
                if match:
                    lexeme = match.group(0)
                    position = match.end()
                    if token_name == "whitespace":
                        break  # Ignore whitespace
                    elif token_name == "brace_comment":
                        if "}" not in lexeme:
                            self.report_error(position, "Unclosed comment block.")
                        break  # Ignore comments
                    elif token_name == "unknown":
                        self.report_error(position, f"Unknown token: {lexeme}")
                    else:
                        self.add_token(token_name, lexeme)
                    break
            if not match:
                self.report_error(position, "Unexpected error in tokenizer.")
                break

    def add_token(self, token_name, lexeme):
        # Add token to the token list
        self.tokens.append({"token": token_name, "lexeme": lexeme})
        
        # Add to symbol table if it is an identifier
        if token_name == "identifier" and lexeme not in KEYWORDS:
            if lexeme not in self.symbol_table:
                self.symbol_table[lexeme] = {"type": "unknown"}

    def report_error(self, position, message):
        line_number = self.source_code[:position].count("\n") + 1
        column_number = position - self.source_code.rfind("\n", 0, position)
        print(f"Error at line {line_number}, column {column_number}: {message}")

    def print_tokens(self):
        print("Tokens:")
        for token in self.tokens:
            print(f"Token: {token['token']}, Lexeme: {token['lexeme']}")

    def print_symbol_table(self):
        print("\nSymbol Table:")
        for name, properties in self.symbol_table.items():
            print(f"Name: {name}, Type: {properties['type']}")

# Example Source Code
source_code = """
LET a = 5
LET b = 10
IF a < b THEN
    LET c = a + b
    LET d = c * 2
ELSE
    LET e = a - b
ENDIF
CALL myFunction(a, b)
"""

# Run Lexical Analyzer
lexer = LexicalAnalyzer(source_code)
lexer.tokenize()
lexer.print_tokens()
lexer.print_symbol_table()
