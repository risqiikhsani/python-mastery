"""
Python Numbers: int, float, complex
"""

# Integer operations
age = 30
year = 2026
print(f"Age: {age}, Year: {year}")

# Float operations
pi = 3.14159
radius = 5.0
area = pi * radius ** 2
print(f"Area of circle: {area:.2f}")

# Complex numbers
z = 2 + 3j
print(f"Complex: {z}, real: {z.real}, imag: {z.imag}")

# Number conversion
print(int(3.7))    # 3 (truncates)
print(round(3.7))  # 4
print(float(10))   # 10.0

# Underscore in numbers (readability)
population = 8_000_000_000
print(f"Population: {population:,}")

# Boolean is subclass of int
print(True + 1)  # 2
print(False + 1)  # 1

# Division
print(10 / 3)   # 3.333... (true division)
print(10 // 3)  # 3 (floor division)
print(10 % 3)   # 1 (modulo)

# Exponentiation
print(2 ** 10)  # 1024