names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

print("=== enumerate() example ===")
for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")

print("\n=== zip() example ===")
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

print("\n=== Combined enumerate() + zip() ===")
for index, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"{index}. {name} -> {score}")

print("\n=== Type checking and conversions ===")
value1 = "500"
value2 = 20.8
value3 = [1, 2, 3]

print(value1, "is of type", type(value1))
print(value2, "is of type", type(value2))
print(value3, "is of type", type(value3))

converted_int = int(value1)
converted_str = str(value2)
converted_tuple = tuple(value3)

print("Converted int:", converted_int, type(converted_int))
print("Converted str:", converted_str, type(converted_str))
print("Converted tuple:", converted_tuple, type(converted_tuple))