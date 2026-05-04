"""
Regular Expressions
"""

import re


# Basic patterns
def basic_patterns():
    text = "Contact: john@example.com or support@company.org"

    # Find email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    print(f"Emails found: {emails}")

    # Search vs match
    match = re.search(r'Contact:', text)  # Finds anywhere
    full_match = re.match(r'Contact:', text)  # Must start at beginning

    # Find all matches
    numbers = re.findall(r'\d+', "Order 123 placed on 2024-01-15")
    print(f"Numbers: {numbers}")

    # Split and sub
    parts = re.split(r'[,\s]+', "apple, banana, cherry")
    print(f"Split: {parts}")

    replaced = re.sub(r'\d+', '#', "Order 123 for item 456")
    print(f"Substituted: {replaced}")


# Compiled patterns (more efficient for reuse)
def compiled_patterns():
    email_regex = re.compile(r'[a-z]+@[a-z]+\.[a-z]+')

    texts = [
        "Email: alice@test.com",
        "Contact bob@company.org",
        "invalid email"
    ]

    for text in texts:
        match = email_regex.search(text)
        if match:
            print(f"Found: {match.group()}")


# Groups and named groups
def groups_demo():
    log = "2024-01-15 10:30:45 ERROR: Connection failed"

    pattern = r'(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>\w+): (?P<message>.*)'

    match = re.match(pattern, log)
    if match:
        print(f"Date: {match.group('date')}")
        print(f"Time: {match.group('time')}")
        print(f"Level: {match.group('level')}")
        print(f"Message: {match.group('message')}")


# Greedy vs non-greedy
def greedy_vs_lazy():
    html = "<div>Hello</div><div>World</div>"

    greedy = re.search(r'<div>.*</div>', html)
    non_greedy = re.search(r'<div>.*?</div>', html)

    print(f"Greedy: {greedy.group()}")       # Matches everything
    print(f"Non-greedy: {non_greedy.group()}")  # Matches first tag only


# Lookahead and lookbehind
def lookaround():
    # Positive lookahead: password must contain digit
    password_pattern = r'\w*(?=\d)'

    # Find word before a number
    text = "apple 5 banana 10 cherry"
    numbers = re.findall(r'\w+(?=\s+\d)', text)
    print(f"Words before numbers: {numbers}")

    # Positive lookbehind
    price_pattern = r'(?<=\\$)\\d+\\.\\d{2}'
    # text = "Item costs $19.99"
    # Find number after $ sign


# Flags
def with_flags():
    text = "Hello\\nWorld"

    case_insensitive = re.findall(r'hello', text, re.IGNORECASE)
    print(f"Case insensitive: {case_insensitive}")

    multiline = re.findall(r'^line', "line1\\nline2\\nline3", re.MULTILINE)
    print(f"Multiline: {multiline}")

    verbose = re.search(r'''
        \\d{3}  # area code
        -      # dash
        \\d{4}  # number
    ''', "123-4567", re.VERBOSE)


# Common patterns
def common_patterns():
    patterns = {
        "phone": r'\d{3}-\d{3}-\d{4}',
        "zip": r'\d{5}(-\d{4})?',
        "date": r'\d{4}-\d{2}-\d{2}',
        "time": r'\d{2}:\d{2}(:\d{2})?',
        "ip": r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
        "url": r'https?://[^\s]+',
    }

    test = "Call 555-123-4567 or visit https://example.com"
    for name, pattern in patterns.items():
        match = re.search(pattern, test)
        if match:
            print(f"{name}: {match.group()}")


basic_patterns()
groups_demo()
greedy_vs_lazy()
common_patterns()