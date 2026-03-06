import re
import json
from pathlib import Path


def to_number(s: str) -> float:
    """
    '1 200,00' -> 1200.00
    '308,00'   -> 308.00
    """
    s = s.replace(" ", "").replace("\xa0", "").replace(",", ".")
    return float(s)


def parse_receipt(text: str) -> dict:
    # 1) Дата/время: "Время: 18.04.2019 11:13:58"
    dt_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})", text)
    date_time = dt_match.group(1) if dt_match else None

    # 2) Оплата (метод): ищем строку "Банковская карта:"
    pay_match = re.search(r"(Банковская\s+карта)\s*:", text, flags=re.IGNORECASE)
    payment_method = pay_match.group(1) if pay_match else None

    # 3) ИТОГО сумма: "ИТОГО:\n18 009,00"
    total_match = re.search(r"ИТОГО:\s*\n\s*([\d\s]+,\d{2})", text)
    total_amount = to_number(total_match.group(1)) if total_match else None

    # 4) Товары: блоки вида:
    # 1.
    # Натрия ...
    # 2,000 x 154,00
    # 308,00
    #
    # Берём:
    # - номер позиции
    # - название (одна строка)
    # - qty и unit_price
    # - line_total (строка с суммой)
    item_pattern = re.compile(
        r"(?m)^\s*(\d+)\.\s*\n"          # номер "1."
        r"(.+?)\s*\n"                   # название товара (одна строка)
        r"([\d,]+)\s*x\s*([\d\s]+,\d{2})\s*\n"  # qty x unit_price
        r"([\d\s]+,\d{2})\s*\n",        # итог по позиции
        flags=re.MULTILINE
    )

    items = []
    for m in item_pattern.finditer(text):
        idx = int(m.group(1))
        name = m.group(2).strip()
        qty = to_number(m.group(3))
        unit_price = to_number(m.group(4))
        line_total = to_number(m.group(5))
        items.append({
            "index": idx,
            "name": name,
            "qty": qty,
            "unit_price": unit_price,
            "line_total": line_total
        })

    # 5) Все цены (просто чтобы “extract all prices” было выполнено):
    # берём все числа формата "1 152,00" или "308,00"
    prices_raw = re.findall(r"\b\d{1,3}(?:[ \xa0]\d{3})*,\d{2}\b", text)
    prices = [to_number(p) for p in prices_raw]

    # 6) Проверка суммой: сумма line_total
    computed_total = round(sum(i["line_total"] for i in items), 2)

    return {
        "date_time": date_time,
        "payment_method": payment_method,
        "total_amount": total_amount,
        "computed_total_from_items": computed_total,
        "items": items,
        "all_prices_found": prices,
        "items_count": len(items),
    }


def main():
    raw_path = Path(__file__).with_name("raw.txt")
    text = raw_path.read_text(encoding="utf-8", errors="ignore")

    result = parse_receipt(text)

    # красивый JSON вывод
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()