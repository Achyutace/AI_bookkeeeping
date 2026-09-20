"""把 excel 账单转换成 data/<user>/entries/ 下的 csv。

- Step1 extract_bill_meta: 读 excel 文件名，过 LLM 提取账户名和账单起止日期
- Step2 map_columns:       excel 过 pandas，过 LLM 把源列名映射到 entries 的列
- Step3 write_entries:     每条记录按自己月份落 entries/YYYY_MM.csv，按秒级时间戳去重，重复的保留最新的

用法::

    python3 script/convert_excel_to_csv.py <excel 路径> [user]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.utils.llm import chat  # noqa: E402

# entries csv 的列顺序，见 data/齐乐辰/entries/
ENTRY_COLUMNS = ["id", "date", "time", "category", "tag", "amount", "account", "status"]

HEAD_ROWS = 20


def _ask_json(prompt: str) -> Dict[str, Any]:
    """问 LLM 要一段 JSON，容忍 ``` 代码块包裹。"""
    text = chat([{"role": "user", "content": prompt}], temperature=0).strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())


STEP1_PROMPT = """下面是一份账单 excel 的文件名，请提取：

- name: 这份账单属于哪个账户，只取简短的平台/银行名，例如 微信、支付宝、农行、招行
- start_date: 账单起始日期，格式 YYYY-MM-DD
- end_date: 账单终止日期，格式 YYYY-MM-DD

文件名里没有的字段就不要出现在结果里。只输出 JSON 对象，不要任何解释。

文件名：{filename}"""


def extract_bill_meta(excel_path) -> Dict[str, Any]:
    """Step1: 从文件名里提取账户名和账单起止日期，提不到的字段不会出现在结果里。"""
    return _ask_json(STEP1_PROMPT.format(filename=Path(excel_path).name))


STEP2_PROMPT = """这是一个账单 excel 的前若干行，用 pandas 以 header=None 读出来的，行号从 0 开始：

{head}

entries 表需要的字段：
- date: 交易日期，例如 2026-09-07
- time: 交易时间，例如 19:19:08
- amount: 交易金额（正数，不带方向）
- direction: 收/支方向，取值形如 支出 / 收入

请找出表头所在的行号，并给出字段到源列名的映射。输出 JSON：

{{
  "header_row": 表头所在的行号,
  "columns": {{"date": "源列名", "time": "源列名", "amount": "源列名", "direction": "源列名"}},
  "expense_values": ["direction 列里表示支出的取值"],
  "income_values": ["direction 列里表示收入的取值"]
}}

某个字段没有对应的源列时，把它写成 null。只输出 JSON 对象，不要任何解释。"""


def map_columns(excel_path, account: str, head_rows: int = HEAD_ROWS) -> pd.DataFrame:
    """Step2: 过 LLM 把源列名映射到 entries 的列。

    返回的 DataFrame 已带 account，id 留空（由 Step3 顺延），category/tag 留空（之后单独打标）。
    """
    raw = pd.read_excel(excel_path, header=None, dtype=object)
    head = raw.head(head_rows).to_csv(index=True, header=False)
    info = _ask_json(STEP2_PROMPT.format(head=head))

    cols = info.get("columns") or {}
    missing = [k for k in ("date", "amount") if not cols.get(k)]
    if missing:
        raise ValueError(f"LLM 没识别出这些列：{', '.join(missing)}")

    body = raw.iloc[int(info["header_row"]) + 1 :].copy()
    body.columns = [str(c).strip() for c in raw.iloc[int(info["header_row"])]]

    stamp = pd.to_datetime(body[cols["date"]], errors="coerce")
    time_col = cols.get("time")
    if time_col:
        # 时分秒单独一列时，只取它的时间部分盖到日期上
        t = pd.to_datetime(body[time_col].astype(str), errors="coerce")
        stamp = stamp.dt.normalize() + (t - t.dt.normalize())

    amount = pd.to_numeric(body[cols["amount"]], errors="coerce").abs()

    # amount 正数表示支出，收入取负
    sign = pd.Series(1, index=body.index)
    dir_col = cols.get("direction")
    if dir_col:
        direction = body[dir_col].astype(str).str.strip()
        income = [str(v).strip() for v in info.get("income_values") or []]
        sign[direction.isin(income)] = -1

    df = pd.DataFrame(
        {
            "id": pd.NA,
            "date": stamp.dt.strftime("%Y-%m-%d"),
            "time": stamp.dt.strftime("%H:%M:%S"),
            "category": "",
            "tag": "",
            "amount": amount * sign,
            "account": account,
            "status": 0,
        }
    )
    return df[ENTRY_COLUMNS].dropna(subset=["date", "amount"]).reset_index(drop=True)


def write_entries(df: pd.DataFrame, entries_dir) -> Dict[str, int]:
    """Step3: 每条记录按自己的月份写进 entries/YYYY_MM.csv。

    同一个月里按秒级时间戳去重，重复的保留最新导入的那条；新条目的 id 在已有最大 id 上顺延。
    返回 {月份: 该月文件的总条数}。
    """
    entries_dir = Path(entries_dir)
    entries_dir.mkdir(parents=True, exist_ok=True)
    result: Dict[str, int] = {}

    for month, part in df.groupby(df["date"].str.slice(0, 7)):
        path = entries_dir / f"{month.replace('-', '_')}.csv"
        if path.exists():
            old = pd.read_csv(path, skipinitialspace=True).reindex(columns=ENTRY_COLUMNS)
        else:
            old = pd.DataFrame(columns=ENTRY_COLUMNS)

        ids = pd.to_numeric(old["id"], errors="coerce")
        next_id = int(ids.max()) + 1 if ids.notna().any() else 1

        merged = pd.concat([old, part], ignore_index=True)
        merged["_ts"] = merged["date"].astype(str) + " " + merged["time"].fillna("").astype(str)
        merged = merged.drop_duplicates(subset="_ts", keep="last")

        fresh = merged["id"].isna()
        merged.loc[fresh, "id"] = range(next_id, next_id + int(fresh.sum()))
        merged["id"] = pd.to_numeric(merged["id"]).astype(int)

        merged = merged.sort_values("_ts", ascending=False).drop(columns="_ts")
        merged[ENTRY_COLUMNS].reset_index(drop=True).to_csv(
            path, index=False, encoding="utf-8-sig"
        )
        result[month] = len(merged)

    return result


def convert(
    excel_path, user: str = "齐乐辰", entries_dir: Optional[str] = None
) -> tuple[Dict[str, Any], Dict[str, int]]:
    """走完三步：提取元信息 -> 映射列名 -> 落盘 entries。"""
    excel_path = Path(excel_path)
    meta = extract_bill_meta(excel_path)
    df = map_columns(excel_path, account=meta.get("name", ""))
    target = Path(entries_dir) if entries_dir else PROJECT_ROOT / "data" / user / "entries"
    return meta, write_entries(df, target)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 script/convert_excel_to_csv.py <excel 路径> [user]")
        return
    user = sys.argv[2] if len(sys.argv) > 2 else "齐乐辰"
    meta, written = convert(sys.argv[1], user)
    print(f"账单信息: {meta}")
    for month, total in sorted(written.items()):
        print(f"{month}: {total} 条")


if __name__ == "__main__":
    main()
