import shutil
from pathlib import Path

source_dir = Path("workspace") / "notes"
target_dir = Path("workspace") / "archived_notes"

source_dir.mkdir(parents=True, exist_ok=True)
target_dir.mkdir(parents=True, exist_ok=True)

source_file = source_dir / "move_me.txt"

# Создаем файл, если его нет
if not source_file.exists():
    source_file.write_text("This file will be moved and copied.", encoding="utf-8")

print(f"Source file created: {source_file}")

# Копирование файла
copied_file = target_dir / "copied_move_me.txt"
shutil.copy(source_file, copied_file)
print(f"File copied to: {copied_file}")

# Перемещение файла
moved_file = target_dir / "moved_move_me.txt"
shutil.move(str(source_file), str(moved_file))
print(f"File moved to: {moved_file}")

print("\n=== Final files in target directory ===")
for item in target_dir.iterdir():
    print(item.name)