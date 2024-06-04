"""
parser.py -- implement simple parser for PMDAS expressions

Accept a string of tokens, return an AST expressed as a stack of dictionaries
"""

"""
    term = number
    expression = term { "+"|"-" term };
"""

from tokenizer import tokenize


def parse_term(tokens):
    """
    term = number
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    raise Exception("Error: number expected.")


def test_parse_term():
    """
    term = number
    """
    tokens = tokenize("2")
    ast, tokens = parse_term(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2


def parse_expression(tokens):
    """
    expression = term { "+" term };
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+","-"]:
        operator = tokens[0]["tag"]
        new_node, tokens = parse_term(tokens[1:])
        node = {"tag": operator, "left": node, "right": new_node}
    return node, tokens


def test_parse_expression():
    """
    expression = term { "+"|"-" term };
    """
    tokens = tokenize("2")
    ast, tokens = parse_term(tokens)
    assert ast == {"tag": "number", "value": 2, "position": 0}
    ast, tokens = parse_expression(tokenize("2+3"))
    assert ast == {
        "tag": "+",
        "left": {"tag": "number", "value": 2, "position": 0},
        "right": {"tag": "number", "value": 3, "position": 2},
    }
    ast, tokens = parse_expression(tokenize("1+2+3"))
    assert ast == {
        "tag": "+",
        "left": {
            "tag": "+",
            "left": {"tag": "number", "value": 1, "position": 0},
            "right": {"tag": "number", "value": 2, "position": 2},
        },
        "right": {"tag": "number", "value": 3, "position": 4},
    }
    ast, tokens = parse_expression(tokenize("3-2"))
    assert ast == {
        "tag": "-",
        "left": {"tag": "number", "value": 3, "position": 0},
        "right": {"tag": "number", "value": 2, "position": 2},
    }

def parse(tokens):
    ast, _ = parse_expression(tokens)
    return ast

def test_parse():
    """
    expression = term { "+" term };
    """
    for expression in ["2","2+2","1+2+3"]:
        tokens = tokenize(expression)
        ast1 = parse(tokens)
        ast2, _ = parse_expression(tokens)
        assert str(ast1) == str(ast2)


if __name__ == "__main__":
    test_parse_term()
    test_parse_expression()
    test_parse()
    print("done.")
