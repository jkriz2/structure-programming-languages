from tokenizer import tokenize
from parser import parse


def evaluate(ast, environment):
    if ast["tag"] == "number":
        assert type(ast["value"]) in [
            float,
            int,
        ], f"unexpected ast numeric value {ast['value']} is a {type(ast['value'])}."
        return ast["value"], False
    if ast["tag"] == "identifier":
        assert (
            type(ast["value"]) is str
        ), f"unexpected ast identifier value {ast['value']} is a {type(ast['value'])}."
        while environment:
            if ast["value"] in environment:
                return environment.get(ast["value"]), False
            else:
                environment = environment.get("$parent", None)
        return None, False
    if ast["tag"] == "if":
        condition, _ = evaluate(ast["condition"], environment)
        if condition:
            value, _ = evaluate(ast["then"], environment)
            return value, False
        if ast.get("else", None):
            value, _ = evaluate(ast["else"], environment)
            return value, False

    if ast["tag"] == "print":
        argument = ast.get("arguments", None)
        while(argument):
            value, _ = evaluate(argument, environment)
            print(value, end = " ")
            argument = argument.get("next", None)
        print()
        return None, False
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
    raise Exception(f"Unknown token in AST: {ast['tag']}")


def equals(code, environment, expected_result, expected_environment=None):
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert (
        result == expected_result
    ), f"""ERROR: When executing-- 
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
    equals("x", {}, None, {})
    equals("x", {"x": 3.0}, 3.0, {"x": 3.0})
    equals("x", {"x": 3.0}, 3.0)
    equals("x", {"x": 3.0, "$parent": {"x": 4.0}}, 3.0)
    equals("x", {"y": 3.0, "$parent": {"x": 4.0}}, 4.0)
    equals("x", {"y": 3.0, "z": 8.0, "$parent": {"y": 4.0, "$parent": {"x": 5.5}}}, 5.5)

def test_evaluate_print_statement():
    print("test evaluate print_statement.")
    equals("print()", {}, None, None)
    equals("print(1)", {}, None, None)
    equals("print(1,2,3)", {}, None, None)


def test_evaluate_if_statement():
    print("test evaluate if statement.")
    equals("if(1) print(1111)", {}, None, None)
    equals("if(0) print(1111) else print(2222)", {}, None, None)


def test_evaluate_addition():
    print("test evaluate addition")
    equals("1+3", {}, 4)
    equals("1+4", {}, 5)
    equals("4+2", {}, 6)
    equals("4+2+1", {}, 7)
    equals("x+y+z", {"x": 3.0, "y": 4.0, "z": 5.0}, 12.0)


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
    equals("(1+2)*3", {}, 9)


if __name__ == "__main__":
    test_evaluate_single_value()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_unary_negation()
    test_evaluate_complex_expression()
    test_evaluate_if_statement()
    test_evaluate_print_statement()
    print("done")
