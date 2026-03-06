import os
from pathlib import Path

base_dir = Path("workspace")
nested_dir = base_dir / "projects" / "python_practice"

# os.makedirs() example
os.makedirs(nested_dir, exist_ok=True)
print(f"Nested directories created: {nested_dir}")

# pathlib mkdir example
another_dir = base_dir / "notes"
another_dir.mkdir(exist_ok=True)
print(f"Another directory created: {another_dir}")

print("\n=== Current working directory ===")
print(os.getcwd())

print("\n=== Listing files and folders in workspace ===")
for item in os.listdir(base_dir):
    print(item)

# Создадим несколько файлов для примера
txt_file = base_dir / "notes" / "info.txt"
py_file = nested_dir / "example.py"

txt_file.write_text("This is a text file.", encoding="utf-8")
py_file.write_text("print('Hello from example.py')", encoding="utf-8")

print("\nExample files created.")

print("\n=== Find files by extension ===")
for path in base_dir.rglob("*"):
    if path.is_file() and path.suffix == ".txt":
        print(f"TXT file found: {path}")
    elif path.is_file() and path.suffix == ".py":
        print(f"PY file found: {path}")