import csv
import sys
from pathlib import Path

from connect import ensure_schema, get_connection


def insert_from_csv(conn, csv_path: Path) -> int:
    inserted = 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fn = (row.get("first_name") or "").strip()
            ln = (row.get("last_name") or "").strip()
            ph = (row.get("phone") or "").strip()
            if not fn or not ph:
                continue
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO contacts (first_name, last_name, phone)
                    VALUES (%s, %s, %s)
                    """,
                    (fn, ln, ph),
                )
            inserted += 1
    conn.commit()
    return inserted


def insert_from_console(conn) -> None:
    first = input("Имя: ").strip()
    last = input("Фамилия (можно пусто): ").strip()
    phone = input("Телефон: ").strip()
    if not first or not phone:
        print("Имя и телефон обязательны.")
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO contacts (first_name, last_name, phone)
                VALUES (%s, %s, %s)
                """,
                (first, last, phone),
            )
        conn.commit()
        print("Контакт добавлен.")
    except Exception as e:
        conn.rollback()
        print("Ошибка:", e)


def update_contact(conn) -> None:
    old_phone = input("Текущий телефон (для поиска записи): ").strip()
    if not old_phone:
        return
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, first_name, last_name, phone FROM contacts WHERE phone = %s",
            (old_phone,),
        )
        row = cur.fetchone()
    if not row:
        print("Контакт с таким телефоном не найден.")
        return
    print(f"Найдено: {row[1]} {row[2]} | {row[3]}")
    field = input("Что меняем? 1 — имя, 2 — телефон: ").strip()
    try:
        with conn.cursor() as cur:
            if field == "1":
                new_name = input("Новое имя: ").strip()
                if not new_name:
                    return
                cur.execute(
                    "UPDATE contacts SET first_name = %s WHERE id = %s",
                    (new_name, row[0]),
                )
            elif field == "2":
                new_phone = input("Новый телефон: ").strip()
                if not new_phone:
                    return
                cur.execute(
                    "UPDATE contacts SET phone = %s WHERE id = %s",
                    (new_phone, row[0]),
                )
            else:
                print("Неверный выбор.")
                return
        conn.commit()
        print("Обновлено.")
    except Exception as e:
        conn.rollback()
        print("Ошибка:", e)


def query_contacts(conn) -> None:
    name_part = input("Фильтр по имени/фамилии (Enter — не использовать): ").strip()
    prefix = input("Префикс телефона, напр. 8707 (Enter — не использовать): ").strip()
    sql = "SELECT id, first_name, last_name, phone FROM contacts WHERE TRUE"
    params = []
    if name_part:
        sql += " AND (first_name ILIKE %s OR last_name ILIKE %s)"
        like = f"%{name_part}%"
        params.extend([like, like])
    if prefix:
        sql += " AND phone LIKE %s"
        params.append(f"{prefix}%")
    sql += " ORDER BY first_name, last_name"
    with conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    if not rows:
        print("Ничего не найдено.")
        return
    for r in rows:
        print(f"  [{r[0]}] {r[1]} {r[2]} | {r[3]}")


def delete_contact(conn) -> None:
    mode = input("Удалить по: 1 — телефону, 2 — имени: ").strip()
    try:
        with conn.cursor() as cur:
            if mode == "1":
                phone = input("Телефон: ").strip()
                if not phone:
                    return
                cur.execute("DELETE FROM contacts WHERE phone = %s RETURNING id", (phone,))
            elif mode == "2":
                name = input("Имя (точное совпадение, без учёта регистра): ").strip()
                if not name:
                    return
                cur.execute(
                    "DELETE FROM contacts WHERE LOWER(first_name) = LOWER(%s) RETURNING id",
                    (name,),
                )
            else:
                print("Неверный выбор.")
                return
            deleted = cur.rowcount
        conn.commit()
        print(f"Удалено записей: {deleted}")
    except Exception as e:
        conn.rollback()
        print("Ошибка:", e)


def print_menu() -> None:
    print(
        """
--- PhoneBook ---
1) Загрузить контакты из CSV
2) Добавить контакт с консоли
3) Изменить имя или телефон
4) Поиск (фильтры по имени и префиксу телефона)
5) Удалить по телефону или имени
6) Показать все контакты
0) Выход
"""
    )


def list_all(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, first_name, last_name, phone FROM contacts ORDER BY first_name"
        )
        rows = cur.fetchall()
    for r in rows:
        print(f"  [{r[0]}] {r[1]} {r[2]} | {r[3]}")


def main() -> None:
    conn = get_connection()
    try:
        ensure_schema(conn)
        default_csv = Path(__file__).with_name("contacts.csv")
        while True:
            print_menu()
            choice = input("Выбор: ").strip()
            if choice == "0":
                break
            if choice == "1":
                path = input(f"Путь к CSV [{default_csv}]: ").strip() or str(default_csv)
                p = Path(path)
                if not p.is_file():
                    print("Файл не найден.")
                    continue
                try:
                    n = insert_from_csv(conn, p)
                    print(f"Добавлено строк: {n}")
                except Exception as e:
                    conn.rollback()
                    print("Ошибка:", e)
            elif choice == "2":
                insert_from_console(conn)
            elif choice == "3":
                update_contact(conn)
            elif choice == "4":
                query_contacts(conn)
            elif choice == "5":
                delete_contact(conn)
            elif choice == "6":
                list_all(conn)
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
