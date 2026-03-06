import re

tests = [
    # 1) 'a' followed by zero or more 'b'
    (r"ab*", ["a", "ab", "abbb"], ["b", "ba", "ac"]),

    # 2) 'a' followed by two to three 'b'
    (r"ab{2,3}", ["abb", "abbb"], ["a", "ab", "abbbb"]),

    # 3) lowercase words joined with underscore
    (r"\b[a-z]+_[a-z]+\b", ["hello_world", "a_b"], ["Hello_world", "a__b"]),

    # 4) one uppercase letter followed by lowercase letters
    (r"\b[A-Z][a-z]+\b", ["Hello", "World"], ["HELLO", "hELlo"]),

    # 5) 'a' followed by anything, ending in 'b'
    (r"a.*b", ["ab", "axb", "a123b"], ["a", "b", "ba"]),

    # 6) replace space/comma/dot with colon
    # (done below separately)

    # 7) snake_case -> camelCase
    # (done below separately)

    # 8) split at uppercase letters
    # (done below separately)

    # 9) insert spaces before capital letters
    # (done below separately)

    # 10) camelCase -> snake_case
    # (done below separately)
]

print("=== Tasks 1-5 quick tests ===")
for pattern, ok, bad in tests[:5]:
    rgx = re.compile(pattern)
    for s in ok:
        print(pattern, s, "=>", bool(rgx.search(s)))
    for s in bad:
        print(pattern, s, "=>", bool(rgx.search(s)))
    print()

print("=== Task 6: replace space/comma/dot with colon ===")
s6 = "Hello, world. I am here"
print(re.sub(r"[ ,\.]", ":", s6))

print("=== Task 7: snake_case to camelCase ===")
def snake_to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])

print(snake_to_camel("my_super_name"))

print("=== Task 8: split at uppercase letters ===")
s8 = "SplitAtUpperCaseLetters"
print(re.findall(r"[A-Z][^A-Z]*", s8))

print("=== Task 9: insert spaces between words starting with capital letters ===")
s9 = "HelloWorldAgain"
print(re.sub(r"(?<!^)([A-Z])", r" \1", s9))

print("=== Task 10: camelCase to snake_case ===")
def camel_to_snake(s: str) -> str:
    return re.sub(r"(?<!^)([A-Z])", r"_\1", s).lower()

print(camel_to_snake("camelCaseString"))