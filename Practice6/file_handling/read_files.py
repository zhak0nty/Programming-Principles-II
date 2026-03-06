from pathlib import Path

file_path = Path("data") / "sample.txt"

if file_path.exists():
    print("=== read() example ===")
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        print(content)

    print("=== readline() example ===")
    with open(file_path, "r", encoding="utf-8") as file:
        first_line = file.readline()
        second_line = file.readline()
        print("First line:", first_line.strip())
        print("Second line:", second_line.strip())

    print("=== readlines() example ===")
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for index, line in enumerate(lines, start=1):
            print(f"Line {index}: {line.strip()}")
else:
    print(f"File does not exist: {file_path}")
    print("Run write_files.py first.")