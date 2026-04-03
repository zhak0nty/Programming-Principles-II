# Practice 8: PhoneBook — PostgreSQL functions and procedures

## Что внутри

| Файл | Назначение |
|------|------------|
| `config.py` | Параметры подключения к PostgreSQL |
| `connect.py` | подключение, таблица `contacts`, выполнение `functions.sql` и `procedures.sql` |
| `functions.sql` | `get_contacts_by_pattern`, `get_contacts_page`, `bulk_insert_contacts` |
| `procedures.sql` | `upsert_contact`, `delete_contact_by_name_or_phone` |
| `phonebook.py` | консольное меню, вызов функций и процедур |
| `contacts.csv` | пример данных для пункта 6 |
| `requirements.txt` | `psycopg2-binary` |
| `run.sh` | запускает `phonebook.py` через venv из корня репозитория |

## Перед запуском

1. Установить **PostgreSQL**, сервис должен слушать порт **5432** (или задать `PGPORT`).
2. Создать базу:
   ```bash
   createdb phonebook_db
   ```
3. Из **корня репозитория** `pp2`:
   ```bash
   ./setup.sh
   ```
4. При необходимости задать пароль:
   ```bash
   export PGPASSWORD=ваш_пароль
   ```

## Запуск

Из корня репозитория:

```bash
cd Practice8
../.venv/bin/python phonebook.py
```

Или:

```bash
./run.sh
```

В Cursor: открой `phonebook.py`, интерпретатор **`.venv/bin/python`**, запуск **F5** (конфигурация «Practice8 phonebook.py»).

## Git

```bash
git add Practice8/
git commit -m "Practice8: PhoneBook with PostgreSQL functions and procedures"
git push origin main
```
