from tokenizer import tokenize
from parser import parse

def evaluate(ast, environment):
    if ast["tag"] == "number":
        assert type(ast["value"]) in [float, int], f"unexpected ast numeric value {ast['value']} is a {type(ast['value'])}."
        return ast["value"], False
    if ast["tag"] == "+":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value + right_value, False
    if ast["tag"] == "-":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value - right_value, False
    if ast["tag"] == "*":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value * right_value, False
    if ast["tag"] == "/":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value / right_value, False
    if ast["tag"] == "negate":
        value, _ = evaluate(ast["value"], environment)
        return -value, False
    if ast["tag"] == "!":
        value, _ = evaluate(ast["value"], environment)
        return not value, False
    if ast["tag"] == "mod":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value % right_value, False
    raise Exception(f"Unknown token in AST: {ast['tag']}")

def equals(code, environment, expected_result, expected_environment=None):
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert (result == expected_result), f"""ERROR: When executing-- 
        {[code]},
        --expected--
        {[expected_result]},
        --got--
        {[result]}."""
    if expected_environment:
        assert (
            environment == expected_environment
        ), f"""
        ERROR: When executing 
        {[code]}, 
        expected
        {[expected_environment]},\n got \n{[environment]}.
        """


def test_evaluate_single_value():
    print("test evaluate single value")
    equals("4", {}, 4, {})


def test_evaluate_addition():
    print("test evaluate addition")
    equals("1+3", {}, 4)
    equals("1+4", {}, 5)
    equals("4+2", {}, 6)
    equals("4+2+1", {}, 7)


def test_evaluate_subtraction():
    print("test evaluate subtraction")
    equals("11-5", {}, 6)


def test_evaluate_multiplication():
    print("test evaluate multiplication")
    equals("11*5", {}, 55)


def test_evaluate_division():
    print("test evaluate division")
    equals("12/3", {}, 4)

def test_evaluate_unary_negation():
    print("test evaluate unary negation")
    equals("-12/3", {}, -4)
    equals("12/-3", {}, -4)
    equals("12/--3", {}, 4)
    equals("(3+4)--(1+2)", {}, 10)

def test_evaluate_complex_expression():
    print("test evaluate complex expression")
    equals("(3+4)-(1+2)", {}, 4)
    equals("3+4*2", {}, 11)
    equals("(1+2)*3",{},9)

def test_evaluate_logical_negation():
    print("test evaluate logical negation")
    equals("!1", {}, 0)
    equals("!0", {}, 1)
    equals("!23", {}, 0)
    equals("!(1)+23", {}, 23)
    equals("!(2*23)", {}, 0)

def test_evaluate_mod():
    print("test evaluate mod")
    equals("10%3", {}, 1)
    equals("10%3*2", {}, 2)
    equals("2*10%3", {}, 2)
    equals("2*11%3", {}, 1)
    equals("2*(11%3)", {}, 4)
    equals("2*!0", {}, 2)
    equals("-11%3", {}, 1)

if __name__ == "__main__":
    test_evaluate_single_value()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_unary_negation()
    test_evaluate_complex_expression()
    test_evaluate_logical_negation()
    test_evaluate_mod()
    print("done")
