"""Validate datapack CSVs against schema/fields.csv.

Checks, for every CSV listed in schema/files.csv:
  - the header matches the schema columns, in order
  - required columns are not empty
  - enum, boolean, integer, number, date and datetime values are well formed
  - the primary key is unique

Run from the repo root:  python3 tools/validate.py [datapack_dir]
Exit code 1 when any error is found.
"""

import csv
import re
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema"

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?\+08:00$")
INT_RE = re.compile(r"^-?\d+$")
NUM_RE = re.compile(r"^-?\d+(\.\d{1,3})?$")
URL_RE = re.compile(r"^https?://\S+$")
OPEN_ENUM_TOKENS = {"speaker_id"}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_value(col, value):
    t = col["type"]
    allowed = [v for v in col["allowed_values"].split("|") if v]
    if t == "enum" and value not in allowed:
        return f"不在允許值 {allowed}"
    if t == "boolean" and value not in ("true", "false"):
        return "必須是 true 或 false"
    if t == "integer" and not INT_RE.match(value):
        return "必須是整數"
    if t == "number" and not NUM_RE.match(value):
        return "必須是數字，最多三位小數"
    if t == "date" and not DATE_RE.match(value):
        return "必須是 YYYY-MM-DD"
    if t == "datetime" and not DATETIME_RE.match(value):
        return "必須是 ISO 8601 且時區為 +08:00"
    if t == "url" and not URL_RE.match(value):
        return "必須是完整網址"
    if t == "url_list" and not all(URL_RE.match(v) for v in value.split(";")):
        return "每個網址都必須完整，以 ; 分隔"
    if t in ("id_list",) and (" " in value or value.endswith(";")):
        return "以 ; 分隔，不加空格"
    if t == "id_list" and allowed and not OPEN_ENUM_TOKENS & set(allowed):
        bad = [v for v in value.split(";") if v not in allowed]
        if bad:
            return f"含不在允許值的項目 {bad}"
    return None


def main():
    pack = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "datapack"
    files = read_csv(SCHEMA / "files.csv")
    by_file = OrderedDict()
    for row in read_csv(SCHEMA / "fields.csv"):
        by_file.setdefault(row["file"], []).append(row)

    errors = []
    checked = 0
    for f in files:
        if f["format"] != "csv":
            continue
        path = pack / f["path"]
        if not path.exists():
            errors.append(f"{f['path']}：檔案不存在")
            continue
        cols = by_file[f["path"]]
        expected = [c["column"] for c in cols]
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            header = next(reader, [])
            rows = list(reader)
        if header != expected:
            errors.append(f"{f['path']}：欄位不符\n    應為 {expected}\n    實際 {header}")
            continue
        keys = [k for k in f["primary_key"].split("+") if k]
        seen = set()
        for i, raw in enumerate(rows, start=2):
            if len(raw) != len(header):
                errors.append(f"{f['path']} 第 {i} 列：欄數 {len(raw)}，應為 {len(header)}")
                continue
            row = dict(zip(header, raw))
            for c in cols:
                v = row[c["column"]]
                if v == "":
                    if c["required"] == "yes":
                        errors.append(f"{f['path']} 第 {i} 列 {c['column']}：必填")
                    continue
                problem = check_value(c, v)
                if problem:
                    errors.append(f"{f['path']} 第 {i} 列 {c['column']}={v!r}：{problem}")
            if keys:
                k = tuple(row[x] for x in keys)
                if k in seen:
                    errors.append(f"{f['path']} 第 {i} 列：主鍵重複 {k}")
                seen.add(k)
        checked += 1

    if errors:
        print(f"檢查 {checked} 張表，發現 {len(errors)} 個問題：")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"OK：{checked} 張表全部符合 schema")


if __name__ == "__main__":
    main()
