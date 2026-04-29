import csv
import json
import sys
from datetime import datetime
from pathlib import Path

from connect import ensure_schema, get_connection


def parse_date(text: str):
    text = text.strip()
    if not text:
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def format_contact_row(row) -> str:
    cid, first_name, last_name, email, birthday, group_name = row
    return (
        f"[{cid}] {first_name} {last_name} | "
        f"email={email or '-'} | birthday={birthday or '-'} | group={group_name or '-'}"
    )


def fetch_phones_map(conn):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT contact_id, phone, type FROM phones ORDER BY contact_id, id"
        )
        rows = cur.fetchall()
    result = {}
    for contact_id, phone, p_type in rows:
        result.setdefault(contact_id, []).append({"phone": phone, "type": p_type})
    return result


def print_contacts_with_phones(conn, rows):
    phones_map = fetch_phones_map(conn)
    if not rows:
        print("Ничего не найдено.")
        return
    for row in rows:
        print(" ", format_contact_row(row))
        for phone_item in phones_map.get(row[0], []):
            print(f"      - {phone_item['phone']} ({phone_item['type']})")


def export_to_json(conn, path: Path) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY c.id
            """
        )
        rows = cur.fetchall()
    phones_map = fetch_phones_map(conn)

    payload = []
    for cid, first_name, last_name, email, birthday, group_name in rows:
        payload.append(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "birthday": birthday.isoformat() if birthday else None,
                "group": group_name,
                "phones": phones_map.get(cid, []),
            }
        )

    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def upsert_contact_from_json(conn, item, on_duplicate: str):
    first_name = (item.get("first_name") or "").strip()
    last_name = (item.get("last_name") or "").strip()
    if not first_name:
        return

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id FROM contacts
            WHERE LOWER(first_name) = LOWER(%s)
              AND LOWER(COALESCE(last_name, '')) = LOWER(%s)
            ORDER BY id
            LIMIT 1
            """,
            (first_name, last_name),
        )
        existing = cur.fetchone()

    if existing and on_duplicate == "skip":
        return

    birthday = parse_date(str(item.get("birthday") or ""))
    email = (item.get("email") or "").strip()
    group_name = (item.get("group") or "Other").strip() or "Other"

    with conn.cursor() as cur:
        cur.execute(
            "CALL upsert_contact_extended(%s, %s, %s, %s, %s, %s, %s)",
            (first_name, last_name, email, birthday, group_name, "", "mobile"),
        )

    if existing and on_duplicate == "overwrite":
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id FROM contacts
                WHERE LOWER(first_name) = LOWER(%s)
                  AND LOWER(COALESCE(last_name, '')) = LOWER(%s)
                ORDER BY id
                LIMIT 1
                """,
                (first_name, last_name),
            )
            contact_id = cur.fetchone()[0]
            cur.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))

    for phone_item in item.get("phones", []):
        phone = (phone_item.get("phone") or "").strip()
        p_type = (phone_item.get("type") or "mobile").strip().lower()
        if phone and p_type in {"home", "work", "mobile"}:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL add_phone(%s, %s, %s)",
                    (f"{first_name} {last_name}".strip(), phone, p_type),
                )


def import_from_json(conn, path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("JSON должен быть массивом объектов.")
        return

    for item in data:
        if not isinstance(item, dict):
            continue
        first_name = (item.get("first_name") or "").strip()
        last_name = (item.get("last_name") or "").strip()
        if not first_name:
            continue

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 1 FROM contacts
                WHERE LOWER(first_name) = LOWER(%s)
                  AND LOWER(COALESCE(last_name, '')) = LOWER(%s)
                LIMIT 1
                """,
                (first_name, last_name),
            )
            duplicate = cur.fetchone() is not None

        decision = "overwrite"
        if duplicate:
            answer = input(
                f"Дубликат {first_name} {last_name}: skip или overwrite? [skip/overwrite]: "
            ).strip().lower()
            decision = "skip" if answer == "skip" else "overwrite"

        upsert_contact_from_json(conn, item, decision)

    conn.commit()
    print("Импорт из JSON завершён.")


def import_from_csv(conn, path: Path) -> None:
    first_names = []
    last_names = []
    emails = []
    birthdays = []
    groups = []
    phones = []
    phone_types = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            first_name = (row.get("first_name") or "").strip()
            if not first_name:
                continue
            first_names.append(first_name)
            last_names.append((row.get("last_name") or "").strip())
            emails.append((row.get("email") or "").strip())
            birthdays.append((row.get("birthday") or "").strip())
            groups.append((row.get("group") or "Other").strip() or "Other")
            phones.append((row.get("phone") or "").strip())
            phone_types.append((row.get("phone_type") or "mobile").strip().lower() or "mobile")

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM bulk_insert_contacts_extended(
                %s::text[], %s::text[], %s::text[], %s::text[],
                %s::text[], %s::text[], %s::text[]
            )
            """,
            (first_names, last_names, emails, birthdays, groups, phones, phone_types),
        )
        bad_rows = cur.fetchall()

    conn.commit()
    if bad_rows:
        print("Ошибки при импорте CSV:")
        for bad in bad_rows:
            print(" ", bad)
    else:
        print("CSV импорт завершён без ошибок.")


def page_loop(conn, limit: int, sort_key: str):
    offset = 0
    while True:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_page(%s, %s, %s)",
                (limit, offset, sort_key),
            )
            rows = cur.fetchall()

        if not rows and offset > 0:
            print("Страниц больше нет, возвращаемся назад.")
            offset = max(0, offset - limit)
            continue

        print(f"\nСтраница (offset={offset}, limit={limit}, sort={sort_key})")
        print_contacts_with_phones(conn, rows)
        cmd = input("Команда [next/prev/quit]: ").strip().lower()
        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break
        else:
            print("Неизвестная команда.")


def choose_sort():
    value = input("Сортировка [name/birthday/date]: ").strip().lower()
    if value in {"name", "birthday", "date"}:
        return value
    return "name"


def main() -> None:
    conn = get_connection()
    try:
        ensure_schema(conn)
        default_csv = Path(__file__).with_name("contacts.csv")
        default_json = Path(__file__).with_name("contacts.json")

        while True:
            print(
                "\n".join(
                    (
                        "\n--- TSIS1 PhoneBook ---",
                        "1) Добавить/обновить контакт",
                        "2) Добавить телефон через процедуру add_phone",
                        "3) Переместить контакт в группу (move_to_group)",
                        "4) Поиск по всем полям (search_contacts)",
                        "5) Фильтр: группа + email + сортировка",
                        "6) Пагинация (next/prev/quit)",
                        "7) Экспорт в JSON",
                        "8) Импорт из JSON (skip/overwrite дубликатов)",
                        "9) Импорт из CSV (extended)",
                        "10) Удалить контакт по имени",
                        "0) Выход",
                    )
                )
            )

            choice = input("Выбор: ").strip()
            if choice == "0":
                break
            if choice == "1":
                first_name = input("Имя: ").strip()
                last_name = input("Фамилия: ").strip()
                email = input("Email: ").strip()
                birthday = parse_date(input("День рождения YYYY-MM-DD: ").strip())
                group_name = input("Группа [Family/Work/Friend/Other]: ").strip() or "Other"
                phone = input("Телефон: ").strip()
                phone_type = input("Тип телефона [home/work/mobile]: ").strip().lower() or "mobile"
                with conn.cursor() as cur:
                    cur.execute(
                        "CALL upsert_contact_extended(%s, %s, %s, %s, %s, %s, %s)",
                        (first_name, last_name, email, birthday, group_name, phone, phone_type),
                    )
                conn.commit()
                print("Контакт сохранён.")
            elif choice == "2":
                contact_name = input("Контакт (Имя Фамилия): ").strip()
                phone = input("Телефон: ").strip()
                p_type = input("Тип [home/work/mobile]: ").strip().lower() or "mobile"
                with conn.cursor() as cur:
                    cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, p_type))
                conn.commit()
                print("Телефон добавлен.")
            elif choice == "3":
                contact_name = input("Контакт (Имя Фамилия): ").strip()
                group_name = input("Новая группа: ").strip()
                with conn.cursor() as cur:
                    cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
                conn.commit()
                print("Группа обновлена.")
            elif choice == "4":
                query = input("Запрос: ").strip()
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
                    rows = cur.fetchall()
                print_contacts_with_phones(conn, rows)
            elif choice == "5":
                group_name = input("Группа (пусто = все): ").strip() or None
                email_pattern = input("Часть email (пусто = все): ").strip() or None
                sort_key = choose_sort()
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM get_contacts_by_filters(%s, %s, %s)",
                        (group_name, email_pattern, sort_key),
                    )
                    rows = cur.fetchall()
                print_contacts_with_phones(conn, rows)
            elif choice == "6":
                limit = int(input("LIMIT [5]: ").strip() or "5")
                sort_key = choose_sort()
                page_loop(conn, limit, sort_key)
            elif choice == "7":
                path = Path(input(f"JSON [{default_json}]: ").strip() or str(default_json))
                export_to_json(conn, path)
                print(f"Экспортировано: {path}")
            elif choice == "8":
                path = Path(input(f"JSON [{default_json}]: ").strip() or str(default_json))
                if not path.is_file():
                    print("JSON файл не найден.")
                    continue
                import_from_json(conn, path)
            elif choice == "9":
                path = Path(input(f"CSV [{default_csv}]: ").strip() or str(default_csv))
                if not path.is_file():
                    print("CSV файл не найден.")
                    continue
                import_from_csv(conn, path)
            elif choice == "10":
                first_name = input("Имя: ").strip()
                last_name = input("Фамилия: ").strip()
                with conn.cursor() as cur:
                    cur.execute("CALL delete_contact_by_name(%s, %s)", (first_name, last_name))
                conn.commit()
                print("Удаление выполнено.")
            else:
                print("Неизвестная команда.")
    finally:
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nВыход.")
        sys.exit(0)
