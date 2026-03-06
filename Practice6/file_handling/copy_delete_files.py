import shutil
from pathlib import Path

data_dir = Path("data")
backup_dir = Path("backup")

data_dir.mkdir(exist_ok=True)
backup_dir.mkdir(exist_ok=True)

source_file = data_dir / "sample.txt"
backup_file = backup_dir / "sample_backup.txt"

if source_file.exists():
    # Копируем файл
    shutil.copy(source_file, backup_file)
    print(f"File copied successfully: {backup_file}")

    # Проверяем, что backup существует
    if backup_file.exists():
        print("Backup file exists.")

    # Безопасное удаление backup файла
    if backup_file.exists():
        backup_file.unlink()
        print(f"Backup file deleted successfully: {backup_file}")
    else:
        print("Backup file was not found for deletion.")
else:
    print(f"Source file not found: {source_file}")
    print("Run write_files.py first.")