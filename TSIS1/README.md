# TSIS1: PhoneBook Extended

## Files

- `phonebook.py` - console app
- `config.py` - PostgreSQL config
- `connect.py` - connection and SQL bootstrap
- `schema.sql` - schema with `groups`, `contacts`, `phones`
- `functions.sql` - search/filter/pagination/bulk functions
- `procedures.sql` - `add_phone`, `move_to_group`, upsert/delete procedures
- `contacts.csv` - sample CSV for extended import

## Run

From repository root:

```bash
cd TSIS1
../.venv/bin/python phonebook.py
```

If password is required:

```bash
export PGPASSWORD=your_password
```
