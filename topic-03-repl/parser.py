"""
parser.py -- implement simple parser for PMDAS expressions

Accept a string of tokens, return an AST expressed as a stack of dictionaries
"""

"""
    simple_expression = number | identifier | "(" expression ")" | "-" simple_expression
    factor = simple_expression;
    term = factor { "*"|"/" factor };
    expression = term { "+"|"-" term };
    expression_list = "(" [ expression { "," expression } ] ")";
    print_statement = "print" 
    statement = expression | print_statement ;
    program = statement;
"""

from tokenizer import tokenize


def parse_simple_expression(tokens):
    """
    simple_expression = number | identifier | "(" expression ")" | "-" simple_expression
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "identifier":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "(":
        node, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "Error: expected ')'"
        return node, tokens[1:]
    if tokens[0]["tag"] == "-":
        new_node, tokens = parse_simple_expression(tokens[1:])
        node = {"tag": "negate", "value": new_node}
        return node, tokens
    return node, tokens

    raise Exception("Error: unexpected token.")


def test_parse_simple_expression():
    """
    simple_expression = number | identifier | "(" expression ")" | "-" simple_expression
    """
    tokens = tokenize("2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    tokens = tokenize("-2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"tag": "number", "value": 2, "position": 1},
    }
    tokens = tokenize("x")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "identifier"
    assert ast["value"] == "x"


def parse_factor(tokens):
    """
    factor = simple_expression;
    """
    return parse_simple_expression(tokens)


def test_parse_factor():
    """
    factor = simple_expression;
    """
    tokens = tokenize("2")
    ast, tokens = parse_factor(tokens)
    tokens = tokenize("2")
    ast2, tokens2 = parse_simple_expression(tokens)
    assert ast == ast2


def parse_term(tokens):
    """
    term = factor { "*"|"/" factor };
    """
    node, tokens = parse_factor(tokens)
    while tokens[0]["tag"] in ["*", "/"]:
        operator = tokens[0]["tag"]
        new_node, tokens = parse_factor(tokens[1:])
        node = {"tag": operator, "left": node, "right": new_node}
    return node, tokens


def test_parse_term():
    """
    term = factor { "*"|"/" factor };
    """
    tokens = tokenize("2")
    ast, tokens = parse_term(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    tokens = tokenize("2*2")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "tag": "*",
        "left": {"tag": "number", "value": 2, "position": 0},
        "right": {"tag": "number", "value": 2, "position": 2},
    }


def parse_expression(tokens):
    """
    expression = term { "+" term };
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+", "-"]:
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
    ast, tokens = parse_expression(tokenize("x+y+z"))
    assert ast == {
        "tag": "+",
        "left": {
            "tag": "+",
            "left": {"tag": "identifier", "value": "x", "position": 0},
            "right": {"tag": "identifier", "value": "y", "position": 2},
        },
        "right": {"tag": "identifier", "value": "z", "position": 4},
    }
    ast, tokens = parse_expression(tokenize("3-2"))
    assert ast == {
        "tag": "-",
        "left": {"tag": "number", "value": 3, "position": 0},
        "right": {"tag": "number", "value": 2, "position": 2},
    }
    ast, tokens = parse_expression(tokenize("1+2*3"))
    assert ast == {
        "tag": "+",
        "left": {"tag": "number", "value": 1, "position": 0},
        "right": {
            "tag": "*",
            "left": {"tag": "number", "value": 2, "position": 2},
            "right": {"tag": "number", "value": 3, "position": 4},
        },
    }
    ast, tokens = parse_expression(tokenize("(1+2)*3"))
    assert ast == {
        "tag": "*",
        "left": {
            "tag": "+",
            "left": {"tag": "number", "value": 1, "position": 1},
            "right": {"tag": "number", "value": 2, "position": 3},
        },
        "right": {"tag": "number", "value": 3, "position": 6},
    }
    ast, tokens = parse_expression(tokenize("-(1+2)*-3"))
    assert ast == {
        "tag": "*",
        "left": {
            "tag": "negate",
            "value": {
                "tag": "+",
                "left": {"tag": "number", "value": 1, "position": 2},
                "right": {"tag": "number", "value": 2, "position": 4},
            },
        },
        "right": {
            "tag": "negate",
            "value": {"tag": "number", "value": 3, "position": 8},
        },
    }


def parse_expression_list(tokens):
    """
    expression_list = "(" [ expression { "," expression } ] ")";
    """
    assert tokens[0]["tag"] == "("
    tokens = tokens[1:]
    first_node = None
    if tokens[0]["tag"] != ")":
        node, tokens = parse_expression(tokens)
        first_node = node
        while tokens[0]["tag"] != ")":
            assert tokens[0]["tag"] == ","
            tokens = tokens[1:]
            node["next"], tokens = parse_expression(tokens)
            node = node["next"]
    assert tokens[0]["tag"] == ")"
    tokens = tokens[1:]
    return first_node, tokens


def test_parse_expression_list():
    ast, tokens = parse_expression_list(tokenize("()"))
    assert ast == None
    ast, tokens = parse_expression_list(tokenize("(1)"))
    assert ast == {"tag": "number", "value": 1, "position": 1}
    ast, tokens = parse_expression_list(tokenize("(1,2,3)"))
    assert ast == {
        "tag": "number",
        "value": 1,
        "position": 1,
        "next": {
            "tag": "number",
            "value": 2,
            "position": 3,
            "next": {"tag": "number", "value": 3, "position": 5},
        },
    }

def parse_if_statement(tokens):
    """
    if_statement = "if" "(" expression ")" statement [ "else" statement ];
    """
    assert tokens[0]["tag"] == "if"
    tokens = tokens[1:]
    assert tokens[0]["tag"] == "("
    tokens = tokens[1:]
    condition, tokens = parse_expression(tokens)
    assert tokens[0]["tag"] == ")"
    tokens = tokens[1:]
    then_statement, tokens = parse_statement(tokens)
    node = {
        "tag":"if",
        "condition":condition,
        "then":then_statement
    }
    if tokens[0]["tag"] == "else":
        tokens = tokens[1:]
        else_statement, tokens = parse_statement(tokens)
        node["else"] = else_statement
    return node, tokens

def test_parse_if_statement():
    """
    if_statement = "if" "(" expression ")" statement [ "else" statement ];
    """
    ast, tokens = parse_if_statement(tokenize("if(1)print(1)"))
    assert ast == {
        "tag": "if",
        "condition": {"tag": "number", "value": 1, "position": 3},
        "then": {
            "tag": "print",
            "arguments": {"tag": "number", "value": 1, "position": 11},
        },
    }
    ast, tokens = parse_if_statement(tokenize("if(1) print(1) else print(2)"))
    assert ast == {
        "tag": "if",
        "condition": {"tag": "number", "value": 1, "position": 3},
        "then": {
            "tag": "print",
            "arguments": {"tag": "number", "value": 1, "position": 12},
        },
        "else": {
            "tag": "print",
            "arguments": {"tag": "number", "value": 2, "position": 26},
        },
    }

def parse_print_statement(tokens):
    """
    print_statement = "print" expression_list
    """
    assert tokens[0]["tag"] == "print"
    tokens = tokens[1:]
    arguments, tokens = parse_expression_list(tokens)
    return {"tag": "print", "arguments": arguments}, tokens


def test_parse_print_statement():
    ast, tokens = parse_print_statement(tokenize("print(4)"))
    assert ast == {
        "tag": "print",
        "arguments": {"tag": "number", "value": 4, "position": 6},
    }
    ast, tokens = parse_print_statement(tokenize("print(1,2,3)"))
    assert ast == {
        "tag": "print",
        "arguments": {
            "tag": "number",
            "value": 1,
            "position": 6,
            "next": {
                "tag": "number",
                "value": 2,
                "position": 8,
                "next": {"tag": "number", "value": 3, "position": 10},
            },
        },
    }


def parse_statement(tokens):
    """
    statement = if_statement | print_statement | expression;
    """
    tag = tokens[0]["tag"]
    if tag == "if":
        return parse_if_statement(tokens)
    if tag == "print":
        return parse_print_statement(tokens)
    return parse_expression(tokens)


def test_parse_statement():
    # print statement
    assert parse_statement(tokenize("print(4)")) == parse_print_statement(
        tokenize("print(4)")
    )

    # expression statements
    assert parse_statement(tokenize("5+3"))[0] == parse_expression(tokenize("5+3"))[0]


def parse_program(tokens):
    """
    programs = statement;
    """
    return parse_statement(tokens)


def test_parse_program():
    # expression statements
    assert parse_program(tokenize("5+3"))[0] == parse_statement(tokenize("5+3"))[0]


def parse(tokens):
    ast, _ = parse_program(tokens)
    return ast


def test_parse():
    """
    expression = term { "+" term };
    """
    for expression in ["2", "2+2", "1+2+3"]:
        tokens = tokenize(expression)
        ast1 = parse(tokens)
        ast2, _ = parse_expression(tokens)
        assert str(ast1) == str(ast2)


if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    test_parse_statement()
    test_parse_expression_list()
    test_parse_if_statement()
    test_parse_print_statement()
    test_parse()
    print("done.")
