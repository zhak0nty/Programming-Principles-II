from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

print("Original numbers:", numbers)

# map() -> применяет функцию к каждому элементу
squared = list(map(lambda x: x ** 2, numbers))
print("Squared numbers using map():", squared)

# filter() -> оставляет только элементы, подходящие под условие
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers using filter():", even_numbers)

# reduce() -> сводит список к одному значению
sum_all = reduce(lambda a, b: a + b, numbers)
print("Sum using reduce():", sum_all)

# Другие built-in функции
print("Length:", len(numbers))
print("Sum:", sum(numbers))
print("Min:", min(numbers))
print("Max:", max(numbers))

# sorted()
unsorted_numbers = [5, 1, 8, 2, 3]
print("Unsorted list:", unsorted_numbers)
print("Sorted list:", sorted(unsorted_numbers))

# type conversion functions
number_str = "123"
converted_number = int(number_str)
print("Converted string to int:", converted_number, type(converted_number))

float_number = float("15.75")
print("Converted string to float:", float_number, type(float_number))