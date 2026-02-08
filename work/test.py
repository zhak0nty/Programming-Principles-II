def is_palindrome(s):
    reversed_s = ""
    for i in range(len(s) - 1, -1, -1):
        reversed_s = reversed_s + s[i]


    if s == reversed_s:
        return True
    else:
        return False


text = input("Введите строку: ")

result = is_palindrome(text)
print(result)