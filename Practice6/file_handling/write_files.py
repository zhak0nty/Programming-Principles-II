from pathlib import Path

# Создаем папку data, если ее нет
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

file_path = data_dir / "sample.txt"

# write mode: "w" -> создает файл заново или перезаписывает
with open(file_path, "w", encoding="utf-8") as file:
    file.write("Hello, this is the first line.\n")
    file.write("Python file handling practice.\n")
    file.write("We are learning how to write into files.\n")

print(f"File created and written successfully: {file_path}")

# append mode: "a" -> добавляет в конец файла
with open(file_path, "a", encoding="utf-8") as file:
    file.write("This line was appended later.\n")
    file.write("Appending does not erase old content.\n")

print("New lines appended successfully.")

# Проверим содержимое
with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

print("\nFinal file content:")
print(content)