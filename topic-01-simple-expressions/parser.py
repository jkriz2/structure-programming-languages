"""
parser.py -- implement simple parser for PMDAS expressions

Accept a string of tokens, return an AST expressed as a stack of dictionaries
"""

"""
    term = number
    expression = term { "+" term };
"""

from tokenizer import tokenize

def parse_term(tokens, environment):
    """
    term = number
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    raise Exception("Error: number expected.")

def test_parse_term():
    print(
    """
    term = number
    """
    )
    t = tokenize("2")
    ast, t = parse_term(t, {})
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    assert t == []

def parse_expression(tokens, environment):
    """
    expression = term { "+" term };
    """
    environment = {}
    ast, tokens = parse_term(tokens, environment) 
    while len(tokens) >= 1 and tokens[0] == "+":
        tokens = tokens[1:]
        term, tokens = parse_term(tokens, environment)
        ast = {
            "tag":"+",
            "left": ast,
            "right" : term 
        }
    pass

def test_parse_single_digit():
    print("test parse single digit")
    environment = {}
    tokens = tokenize("2")
    ast = parse_expression(tokens, environment)

if __name__ == "__main__":
    test_parse_term()
