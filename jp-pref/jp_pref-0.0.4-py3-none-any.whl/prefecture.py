# AUTOGENERATED! DO NOT EDIT! File to edit: 10_pref.ipynb (unless otherwise specified).

__all__ = ['names', 'short_names', 'df', '__code2name']

# Cell
from typing import List

from fastcore.basics import patch
from fastcore.dispatch import typedispatch

# Cell


import pandas as pd

# 都道府県正式名称
names = [
    "北海道",
    "青森県",
    "岩手県",
    "宮城県",
    "秋田県",
    "山形県",
    "福島県",
    "茨城県",
    "栃木県",
    "群馬県",
    "埼玉県",
    "千葉県",
    "東京都",
    "神奈川県",
    "新潟県",
    "富山県",
    "石川県",
    "福井県",
    "山梨県",
    "長野県",
    "岐阜県",
    "静岡県",
    "愛知県",
    "三重県",
    "滋賀県",
    "京都府",
    "大阪府",
    "兵庫県",
    "奈良県",
    "和歌山県",
    "鳥取県",
    "島根県",
    "岡山県",
    "広島県",
    "山口県",
    "徳島県",
    "香川県",
    "愛媛県",
    "高知県",
    "福岡県",
    "佐賀県",
    "長崎県",
    "熊本県",
    "大分県",
    "宮崎県",
    "鹿児島県",
    "沖縄県",
]

# Cell
# 都道府県の略名
short_names = [p[:-1] for p in names]
# 都道府県データフレーム. Index に日本都道府県コード（JIS X 0401-1973）を設定
df = pd.DataFrame(
    dict(
        name=names,
        short_name=short_names,
    ),
    index=pd.Index(range(1, 1 + len(names)), name="code"),
)

# Cell
__code2name = {
    code: name
    for name, code in zip(df.name, df.index)
}

# Internal Cell
__name2code = {
    **{name: code for name, code in zip(df.name, df.index)},
    **{name: code for name, code in zip(df.short_name, df.index)},
}

# Cell

@typedispatch
def name2code(name: str) -> int:
    """ Convert prefecture name to code """
    return __name2code[name]

@typedispatch
def name2code(arr: List) -> List:
    """ Convert a list of prefecture name to codes """
    return [__name2code[e] for e in arr]

@typedispatch
def name2code(s: pd.Series) -> pd.Series:
    """ Convert a pandas series of prefecture name to codes """
    return s.map(__name2code)

# Cell

@typedispatch
def code2name(code: int) -> str:
    """ Convert prefecture code to name """
    return __code2name[code]

@typedispatch
def code2name(arr: List) -> List:
    """ Convert a list of prefecture code to names """
    return [__code2name[e] for e in arr]

@typedispatch
def code2name(s: pd.Series) -> pd.Series:
    """ Convert a pandas series of prefecture code to names """
    return s.map(__code2name)