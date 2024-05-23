# tokenizer

"""
break character stream into tokens, provide a list of tokens

    tokens = tokenize(string_of_code)
"""

import re

patterns = [["\+", "+"], ["\*", "*"], ["\d+", "number"]]

for pattern in patterns:
    pattern[0] = re.compile(pattern[0])


def tokenize(characters):
    tokens = []
    position = 0
    while position < len(characters):
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                break
        assert match
        # update position for next match
        token = {
            "tag": tag,
            "value": match.group(0),
            "position": match.end(),
        }
        if token["tag"] == "number":
            if "." in token["value"]:
                token["value"] == float(token["value"])
            else:
                token["value"] == int(token["value"])
        position = match.end()
        tokens.append(token)
    return tokens


def test_simple_tokens():
    print("testing simple tokens")
    assert tokenize("") == []
    assert tokenize("*")[0]["tag"] == "*"
    tokens = tokenize("*+")
    assert tokens == [
        {"tag": "*", "value": "*", "position": 1},
        {"tag": "+", "value": "+", "position": 2},
    ]
    tokens = tokenize("123")
    assert tokens == [{"tag": "number", "value": "123", "position": 3}]


if __name__ == "__main__":
    test_simple_tokens()
    print("done.")
