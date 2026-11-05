"""Build the datapack skeleton from schema/.

Generates, from schema/files.csv, schema/fields.csv and schema/parameters.csv:
  - datapack/<path>.csv        header row only, columns in schema order
  - datapack/manifest.csv      one row per file, status = pending
  - datapack/docs/field_reference.md

Hand-written Markdown files in datapack/ are never overwritten.
Run from the repo root:  python3 tools/build.py
"""

import csv
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema"
PACK = ROOT / "datapack"

TYPE_NOTES = OrderedDict([
    ("string", "文字"),
    ("integer", "整數"),
    ("number", "數字，小數點用 .，最多三位小數"),
    ("boolean", "true 或 false（小寫）"),
    ("enum", "只能填「允許值」中的一個"),
    ("id", "代號，格式見定義"),
    ("id_list", "多個代號，以 ; 分隔，不加空格"),
    ("url", "完整網址，含 https://"),
    ("url_list", "多個網址，以 ; 分隔"),
    ("date", "YYYY-MM-DD"),
    ("datetime", "ISO 8601，含時區 +08:00，例如 2026-11-12T13:05:00+08:00"),
])

REQUIRED_NOTES = {
    "yes": "必填",
    "no": "可留空",
    "conditional": "條件必填（條件寫在定義中）",
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load():
    files = read_csv(SCHEMA / "files.csv")
    fields = read_csv(SCHEMA / "fields.csv")
    params = read_csv(SCHEMA / "parameters.csv")
    by_file = OrderedDict()
    for row in fields:
        by_file.setdefault(row["file"], []).append(row)
    return files, by_file, params


def check(files, by_file):
    errors = []
    paths = {f["path"] for f in files}
    for path in by_file:
        if path not in paths:
            errors.append(f"fields.csv 有 {path}，但 files.csv 沒有")
    for f in files:
        if f["format"] == "csv" and f["path"] not in by_file:
            errors.append(f"{f['path']} 是 CSV，但 fields.csv 沒有欄位")
    for path, cols in by_file.items():
        seen = set()
        for c in cols:
            name = c["column"]
            if name in seen:
                errors.append(f"{path} 欄位重複：{name}")
            seen.add(name)
            if c["type"] not in TYPE_NOTES:
                errors.append(f"{path}.{name} 型別不明：{c['type']}")
            if c["required"] not in REQUIRED_NOTES:
                errors.append(f"{path}.{name} required 不明：{c['required']}")
            if c["type"] == "enum" and not c["allowed_values"]:
                errors.append(f"{path}.{name} 是 enum 但沒有允許值")
            if not name.replace("_", "").isalnum() or name != name.lower():
                errors.append(f"{path}.{name} 欄位名不是小寫 snake_case")
    return errors


def write_headers(files, by_file):
    for f in files:
        if f["format"] != "csv" or f["path"] == "manifest.csv":
            continue
        out = PACK / f["path"]
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", newline="", encoding="utf-8") as fh:
            csv.writer(fh, lineterminator="\n").writerow(
                [c["column"] for c in by_file[f["path"]]]
            )


def write_dirs(files):
    for f in files:
        if f["format"] == "dir":
            d = PACK / f["path"]
            d.mkdir(parents=True, exist_ok=True)
            keep = d / ".gitkeep"
            if not any(p for p in d.iterdir() if p.name != ".gitkeep"):
                keep.touch()


def write_manifest(files, by_file):
    cols = [c["column"] for c in by_file["manifest.csv"]]
    out = PACK / "manifest.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        for f in files:
            w.writerow({
                "path": f["path"],
                "title_zh": f["title_zh"],
                "version_added": f["version"],
                "status": "pending",
                "row_count": "",
                "source_devices": f["source_devices"],
                "method": "",
                "updated_at": "",
                "sha256": "",
                "note": "",
            })


def md_escape(text):
    return text.replace("|", "\\|")


def write_reference(files, by_file, params):
    lines = []
    lines.append("# 欄位說明")
    lines.append("")
    lines.append("本檔由 `tools/build.py` 依 `schema/` 產生，請勿手動修改；要改欄位請改 `schema/fields.csv` 後重新產生。")
    lines.append("")
    lines.append("## 共通規則")
    lines.append("")
    lines.append("- **檔案格式**：CSV 一律 UTF-8（不含 BOM）、逗號分隔、換行為 LF、第一列為欄位名；含逗號、引號或換行的值用雙引號包起來（RFC 4180）。")
    lines.append("- **命名**：檔名、資料夾名與欄位名一律英文小寫，以 `_` 連接。")
    lines.append("- **時間軸**：`t_sec` 是從 T0 起算的秒數，T0 是開場第一段掌聲在主收音設備上的起點，T0 以前為負數；所有裝置以同一個聲音事件對時。`*_clock` 是同一時刻的台北時間。")
    lines.append("- **區間**：`start_t_sec` 到 `end_t_sec` 是左閉右開區間 [start, end)。")
    lines.append("- **空值與零**：沒測到、不適用或畫面不可用時留空；`0` 代表有測，結果是零。")
    lines.append("- **計數是下限**：遮擋會造成低估，所有人數欄位代表「至少」。")
    lines.append("- **面積法**：影像只算座位區的面積比例，不跑骨架、不認臉、不追個人；分不出手或手機，一律稱「舉起來」。")
    lines.append("- **個資**：不收觀眾的姓名、臉、聯絡方式與帳號；姓名只限同意公開的講者；問題與題目改寫時移除身分線索。")
    lines.append("- **不放判斷**：只放觀察值與照公開規則算出的結果；重點、金句等判斷放報告。")
    lines.append("- **參數**：定義中出現的參數名（例如 `polite_window_sec`）見文末參數表。")
    lines.append("")
    lines.append("## 欄位型別")
    lines.append("")
    lines.append("| 型別 | 格式 |")
    lines.append("| --- | --- |")
    for t, note in TYPE_NOTES.items():
        lines.append(f"| `{t}` | {note} |")
    lines.append("")
    lines.append("必填欄：" + "；".join(f"`{k}` {v}" for k, v in REQUIRED_NOTES.items()) + "。")
    lines.append("")
    lines.append("## 檔案總覽")
    lines.append("")
    lines.append("| 檔案 | 中文名稱 | 版本 | 一列代表 | 主鍵 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for f in files:
        lines.append(
            f"| `{f['path']}` | {f['title_zh']} | {f['version']} | {f['grain'] or '—'} | "
            f"{('`' + f['primary_key'] + '`') if f['primary_key'] else '—'} |"
        )
    lines.append("")
    for f in files:
        if f["path"] not in by_file:
            continue
        lines.append(f"## `{f['path']}`：{f['title_zh']}")
        lines.append("")
        lines.append(f"{f['description']}。")
        lines.append("")
        meta = [f"版本：{f['version']}", f"一列代表：{f['grain']}"]
        if f["primary_key"]:
            meta.append(f"主鍵：`{f['primary_key']}`")
        if f["source_devices"]:
            meta.append(f"來源設備：{f['source_devices']}")
        lines.append("　".join(meta))
        lines.append("")
        lines.append("| 欄位 | 型別 | 必填 | 單位 | 允許值 | 定義 | 範例 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for c in by_file[f["path"]]:
            allowed = " / ".join(f"`{v}`" for v in c["allowed_values"].split("|")) if c["allowed_values"] else ""
            example = f"`{md_escape(c['example'])}`" if c["example"] else ""
            lines.append(
                f"| `{c['column']}` | {c['type']} | {REQUIRED_NOTES[c['required']]} | {c['unit']} | "
                f"{allowed} | {md_escape(c['definition'])} | {example} |"
            )
        lines.append("")
    lines.append("## 參數")
    lines.append("")
    lines.append("狀態：`fixed` 已定；`to_test` 由測試定；`to_decide` 由負責人決定。定案後改 `schema/parameters.csv` 並寫進 CHANGELOG。")
    lines.append("")
    lines.append("| 參數 | 值 | 單位 | 用在 | 定義 | 狀態 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for p in params:
        lines.append(
            f"| `{p['name']}` | {p['value']} | {p['unit']} | `{p['used_by']}` | {md_escape(p['definition'])} | {p['status']} |"
        )
    lines.append("")
    out = PACK / "docs" / "field_reference.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def main():
    files, by_file, params = load()
    errors = check(files, by_file)
    if errors:
        print("schema 有錯誤：")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    write_headers(files, by_file)
    write_dirs(files)
    write_manifest(files, by_file)
    write_reference(files, by_file, params)
    n_csv = sum(1 for f in files if f["format"] == "csv")
    n_cols = sum(len(v) for v in by_file.values())
    print(f"OK：{len(files)} 個檔案、{n_csv} 張 CSV、{n_cols} 個欄位")


if __name__ == "__main__":
    main()
