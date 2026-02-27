import json
from pathlib import Path


def find_sample_file() -> Path:
    here = Path(__file__).resolve().parent
    candidates = [
        here / "sample-data.json",
        here / "Practice 04" / "exercises" / "json" / "sample-data.json",
        here / "exercises" / "json" / "sample-data.json",
        here / "Practice_04" / "exercises" / "json" / "sample-data.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(
        "Не найден sample-data.json. Положи его рядом с json.py "
        "или в exercises/json/sample-data.json"
    )


def load_interfaces(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    imdata = data.get("imdata", [])
    rows = []
    for item in imdata:
        obj = item.get("l1PhysIf", {})
        attrs = obj.get("attributes", {})
        dn = attrs.get("dn", "")
        descr = attrs.get("descr", "")
        speed = attrs.get("speed", "")
        mtu = attrs.get("mtu", "")
        rows.append((dn, descr, speed, mtu))
    return rows


def print_table(rows):
    print("Interface Status")
    print("=" * 78)
    print(f'{"DN":<55} {"Description":<14} {"Speed":<6} {"MTU":<5}')
    print("-" * 78)

    for dn, descr, speed, mtu in rows:
        print(f"{dn:<55} {descr:<14} {speed:<6} {mtu:<5}")


if __name__ == "__main__":
    path = find_sample_file()
    rows = load_interfaces(path)
    print_table(rows)