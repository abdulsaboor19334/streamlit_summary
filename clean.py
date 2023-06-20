from base64 import b64encode
import pandas as pd
import numpy as np
import os

def to_float(num):
    try:
        return float(num)
    except:
        return np.nan

def clean(df):
    df.columns = [str(x).strip().lower().replace(" ","_") for x in df.iloc[0]]

    # select columns
    df = df[[
    "date",
    "order_number",
    "phone_number",
    "sku_name",
    "sku_code",
    "quantity",
    "shop_price",
    "shop_total"
    ]]
    df.drop(0,inplace=True)

    # convert to float or null
    cols = [
        "shop_price",
        "shop_total",
        "quantity"
        ]
    for col in cols:
        df[col] = df[col].apply(to_float)

    df = df.loc[(~df["shop_total"].isna())&(df["shop_total"]!=0)]
    df["order_number"] = [b64encode(os.urandom(11)).decode() for x in range(len(df["order_number"]))]
    df["phone_number"] = [b64encode(os.urandom(11)).decode() for x in range(len(df["phone_number"]))]

    df.shop_price.dropna(how="any",inplace=True)

    df["date"] = pd.to_datetime(df["date"],format="%d/%m/%Y")

    return df