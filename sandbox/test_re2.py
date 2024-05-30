import re

# Define the regular expression pattern
pattern = r"\d+(\.\d*)?|\.\d+"

# Test cases and expected results
test_cases = {
    "123": True,
    "123.456": True,
    ".456": True,
    "123.": True,
    ".": False,
    "abc": False,
    "12a34": False,
    "12.34.56": False,
    "": False,
}


# Function to test the regex pattern
def test_regex():
    compiled_pattern = re.compile(pattern)
    for test, expected in test_cases.items():
        match = bool(compiled_pattern.fullmatch(test))
        assert (
            match == expected
        ), f"Test case '{test}' failed: expected {expected}, got {match}"


if __name__ == "__main__":
    test_regex()
    print("All tests passed.")
