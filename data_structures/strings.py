"""
Python Strings: creation, methods, formatting
"""

# Creation
s1 = "double quotes"
s2 = 'single quotes'
s3 = """multi-line
string"""

# f-strings (preferred)
name = "Alice"
age = 30
print(f"Hello, {name}. You are {age}.")

# Format specifiers
pi = 3.14159
print(f"Pi: {pi:.2f}")  # Pi: 3.14
print(f"Pad: {42:05d}")  # Pad: 00042

# String methods
msg = "  Hello, World!  "
print(msg.strip())      # Hello, World!
print(msg.lower())      #   hello, world!
print(msg.upper())      #   HELLO, WORLD!
print(msg.replace("World", "Python"))

# Split and join
sentence = "the quick brown fox"
words = sentence.split(" ")
print(words)  # ['the', 'quick', 'brown', 'fox']
joined = "-".join(words)
print(joined)  # the-quick-brown-fox

# Check methods
print("abc".isalpha())   # True
print("123".isdigit())   # True
print("abc123".isalnum())  # True

# Slicing
text = "Hello, World!"
print(text[0:5])    # Hello
print(text[-6:-1])  # World
print(text[::2])    # Hlo ol!


# String multiplication
print("-" * 20)  # --------------------

# Membership
print("World" in text)  # True
print("Python" in text)  # False

# Escape characters
print("Line1\nLine2")
print("Tab\tColumn")
print('She said: "Hi"')