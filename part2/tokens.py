from enum import Enum

class Token(Enum):
    ID     = "ID"
    NUM    = "NUM"
    HNUM   = "HNUM"

    INCR   = "INCR"
    PLUS   = "PLUS"
    MULT   = "MULT"
    SEMI   = "SEMI"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    ASSIGN = "ASSIGN"

    IF     = "IF"
    ELSE   = "ELSE"
    WHILE  = "WHILE"
    INT    = "INT"
    FLOAT  = "FLOAT"

    IGNORE = "IGNORE"

class Lexeme:
    def __init__(self, token:Token, value:str) -> None:
        self.token = token
        self.value = value

    def __str__(self):
        return "(" + str(self.token) + "," + "\"" + self.value + "\"" + ")"

def idy(l:Lexeme) -> Lexeme:
    return l

# Keyword handling is done as an action on ID tokens
def id_or_kw(l:Lexeme) -> Lexeme:
    if l.value == "if":
        return Lexeme(Token.IF, l.value)
    if l.value == "else":
        return Lexeme(Token.ELSE, l.value)
    if l.value == "while":
        return Lexeme(Token.WHILE, l.value)
    if l.value == "int":
        return Lexeme(Token.INT, l.value)
    if l.value == "float":
        return Lexeme(Token.FLOAT, l.value)
    return l

tokens = [
    # Multi-char operators / special forms first
    (Token.INCR,   r"\+\+",                 idy),

    # Keywords handled via ID token action (keep ID before NUM is OK; NUM starts w/ digit anyway)
    # ID: letters/digits, cannot start with digit
    (Token.ID,     r"[A-Za-z][A-Za-z0-9]*", id_or_kw),

    # Hex numbers: 0x followed by 1+ hex digits (case-insensitive A-F)
    (Token.HNUM,   r"0[xX][0-9a-fA-F]+",    idy),

    # NUM: integer OR optional leading digits + '.' + digits after dot
    # Accepts: 56, 56.7, .7
    # Rejects: 56., .
    (Token.NUM,    r"(?:[0-9]+|[0-9]*\.[0-9]+)", idy),

    # Single-char tokens
    (Token.PLUS,   r"\+",                   idy),
    (Token.MULT,   r"\*",                   idy),
    (Token.SEMI,   r";",                    idy),
    (Token.LPAREN, r"\(",                   idy),
    (Token.RPAREN, r"\)",                   idy),
    (Token.LBRACE, r"\{",                   idy),
    (Token.RBRACE, r"\}",                   idy),
    (Token.ASSIGN, r"=",                    idy),

    # Ignore whitespace/newlines (consume runs)
    (Token.IGNORE, r"[ \n]+",               idy),
]