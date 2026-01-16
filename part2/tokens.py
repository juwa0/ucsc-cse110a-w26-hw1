from enum import Enum

class Token(Enum):
    ID     = "ID"
    NUM    = "NUM"
    IGNORE = "IGNORE"

class Lexeme:
    def __init__(self, token:Token, value:str) -> None:
        self.token = token
        self.value = value

    def __str__(self):
        return "(" + str(self.token) + "," + "\"" + self.value + "\"" + ")"    

def idy(l:Lexeme) -> Lexeme:
    return l

tokens = [
    (Token.ID,     "[a-z]+",  idy),
    (Token.NUM,    "[0-9]+",  idy),
    (Token.IGNORE, " |\n",    idy)
]
