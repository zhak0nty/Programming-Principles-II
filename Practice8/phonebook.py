import csv
import sys
from pathlib import Path

from connect import ensure_schema, get_connection


def main() -> None:
    conn = get_connection()
    try:
        ensure_schema(conn)
        default_csv = Path(__file__).with_name("contacts.csv")
        while True:
            print(
                "\n".join(
                    (
                        "--- PhoneBook ---",
                        "1) Поиск по шаблону",
                        "2) Добавить или обновить контакт",
                        "3) Массовая вставка из списков",
                        "4) Постраничный вывод",
                        "5) Удалить контакт",
                        "6) Загрузить CSV в таблицу",
                        "0) Выход",
                    )
                )
            )
            choice = input("Выбор: ").strip()
            if choice == "0":
                break
            if choice == "1":
                p = input("Шаблон (имя, фамилия или телефон): ").strip()
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM get_contacts_by_pattern(%s)",
                        (p,),
                    )
                    rows = cur.fetchall()
                for r in rows:
                    print(f"  [{r[0]}] {r[1]} {r[2]} | {r[3]}")
                if not rows:
                    print("Ничего не найдено.")
            elif choice == "2":
                fn = input("Имя: ").strip()
                ln = input("Фамилия: ").strip()
                ph = input("Телефон: ").strip()
                with conn.cursor() as cur:
                    cur.execute(
                        "CALL upsert_contact(%s, %s, %s)",
                        (fn, ln, ph),
                    )
                conn.commit()
                print("Готово.")
            elif choice == "3":
                print("Введите строки: Имя|Фамилия|Телефон, пустая строка — конец.")
                fns, lns, phs = [], [], []
                while True:
                    line = input().strip()
                    if not line:
                        break
                    parts = line.split("|")
                    if len(parts) < 3:
                        print("Нужно: Имя|Фамилия|Телефон")
                        continue
                    fns.append(parts[0].strip())
                    lns.append(parts[1].strip())
                    phs.append(parts[2].strip())
                if not fns:
                    print("Нет данных.")
                    continue
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM bulk_insert_contacts(%s::text[], %s::text[], %s::text[])",
                        (fns, lns, phs),
                    )
                    bad = cur.fetchall()
                conn.commit()
                if bad:
                    print("Ошибочные строки:")
                    for b in bad:
                        print(f"  {b}")
                else:
                    print("Все строки успешно вставлены.")
            elif choice == "4":
                lim = int(input("LIMIT: ").strip() or "10")
                off = int(input("OFFSET: ").strip() or "0")
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT * FROM get_contacts_page(%s, %s)",
                        (lim, off),
                    )
                    rows = cur.fetchall()
                for r in rows:
                    print(f"  [{r[0]}] {r[1]} {r[2]} | {r[3]}")
            elif choice == "5":
                mode = input("По телефону? (y/n): ").strip().lower()
                by_phone = mode.startswith("y")
                if by_phone:
                    ph = input("Телефон: ").strip()
                    fn = ""
                else:
                    ph = ""
                    fn = input("Имя: ").strip()
                with conn.cursor() as cur:
                    cur.execute(
                        "CALL delete_contact_by_name_or_phone(%s, %s, %s)",
                        (by_phone, fn, ph),
                    )
                conn.commit()
                print("Удаление выполнено.")
            elif choice == "6":
                path = input(f"CSV [{default_csv}]: ").strip() or str(default_csv)
                p = Path(path)
                if not p.is_file():
                    print("Файл не найден.")
                    continue
                n = 0
                with open(p, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        fn = (row.get("first_name") or "").strip()
                        ln = (row.get("last_name") or "").strip()
                        ph = (row.get("phone") or "").strip()
                        if not fn or not ph:
                            continue
                        with conn.cursor() as cur:
                            cur.execute(
                                "INSERT INTO contacts (first_name, last_name, phone) VALUES (%s, %s, %s)",
                                (fn, ln, ph),
                            )
                        n += 1
                conn.commit()
                print(f"Добавлено строк: {n}")
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
