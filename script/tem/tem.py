"""excel(xlsx) -> csv 转换。

读取时用 header=None，保住账单前 15 行的元信息；样式标成日期格式的列
（微信的交易时间是 Excel 序列号）由 pandas 直接还原成 datetime。
"""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_SRC = (
    PROJECT_ROOT
    / "data/齐乐辰/raw_data/微信/微信支付账单流水文件(20260607-20260907)_20260907190315.xlsx"
)


def xlsx_to_csv(src, dst=None, encoding="utf-8-sig"):
    """src: xlsx 路径；dst: csv 路径，缺省是 src 同目录同名 .csv。返回写出路径。"""
    src = Path(src)
    dst = Path(dst) if dst else src.with_suffix(".csv")

    pd.read_excel(src, header=None, dtype=object).to_csv(
        dst, index=False, header=False, encoding=encoding
    )
    return dst


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    dst = (
        Path(sys.argv[2])
        if len(sys.argv) > 2
        else PROJECT_ROOT / src.with_suffix(".csv").name
    )
    out = xlsx_to_csv(src, dst)
    print(f"{src}\n-> {out}")


if __name__ == "__main__":
    main()


"""
作用是把 excel 文件转换为 csv 文件
param:
- excel_path: excel 文件路径
- csv_path: csv 文件路径

Step1: 读取 excel 文件名，AI提取名字、起始日期、终止日期，如果没有的话不要写
Step2: 把 excel 转 pandas，过一遍AI处理列名，看哪些列名和我的csv对应
Step3: 把pandas塞进/Users/achyutace/Desktop/记账/data/齐乐辰/entries，按照月份排布账单，按照时间逻辑自动去重（按秒级时间戳），如果有重复的就保留最新的那条

列名参考/Users/achyutace/Desktop/记账/data/齐乐辰/entries/2026_09-2026_10.csv

"""