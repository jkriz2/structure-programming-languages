import re

# Define the regular expression pattern
pattern = r"\d+(\.\d*)?|\.\d+"

# Test cases
test_cases = ["123", "123.456", ".456", "123.", ".", "abc", "12a34", "12.34.56", ""]


# Function to test the regex pattern
def test_regex(pattern, test_cases):
    compiled_pattern = re.compile(pattern)
    for test in test_cases:
        match = compiled_pattern.fullmatch(test)
        if match:
            print(f"'{test}' matches")
        else:
            print(f"'{test}' does not match")


# Run the test
test_regex(pattern, test_cases)
