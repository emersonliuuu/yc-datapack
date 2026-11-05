"""Package datapack/ for release.

Usage: python3 tools/package.py <version> [out_dir]

- Runs validate.py first; stops if any check fails.
- Leaves out files marked internal in schema/files.csv (e.g. file_owners.csv),
  plus .gitkeep and the Markdown template files that start with "_".
- Writes datapack_yc_taipei_1112_<version>.zip.
"""
import csv
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT / "datapack"
SCHEMA = ROOT / "schema"


def main():
    if len(sys.argv) < 2:
        print("用法：python3 tools/package.py <version> [out_dir]")
        sys.exit(1)
    version = sys.argv[1]
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "dist"
    result = subprocess.run([sys.executable, str(ROOT / "tools" / "validate.py"), str(PACK)])
    if result.returncode != 0:
        print("validate.py 沒過，不打包")
        sys.exit(1)
    with open(SCHEMA / "files.csv", newline="", encoding="utf-8-sig") as fh:
        internal = {r["path"] for r in csv.DictReader(fh) if r["internal"] == "true"}
    out_dir.mkdir(parents=True, exist_ok=True)
    name = f"datapack_yc_taipei_1112_{version}"
    out = out_dir / f"{name}.zip"
    kept, skipped = 0, []
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(PACK.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(PACK).as_posix()
            if rel in internal or path.name == ".gitkeep" or path.name.startswith("_"):
                skipped.append(rel)
                continue
            zf.write(path, f"{name}/{rel}")
            kept += 1
    print(f"OK：{out}（{kept} 個檔案）")
    print("沒有打包：" + "、".join(skipped))


if __name__ == "__main__":
    main()
