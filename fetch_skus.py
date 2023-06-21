import pandas as pd
import numpy as np

def assign_name(series):
    try:
        return catagories.loc[catagories.category_id == max(series)].category_name
    except KeyError:
        return np.nan

def get_skus():
    global catagories
    path = "./sku_category_mapping.csv" 
    sku_data = pd.read_csv(path)

    catagories = sku_data.groupby("category_id", as_index=False).agg(
        category_name = pd.NamedAgg(column="category_name",aggfunc="first")
    )

    sku_per_catagroy = sku_data.groupby("sku", as_index=False).agg(
        category_id = pd.NamedAgg(column="category_id",aggfunc="max"),
        category_name = pd.NamedAgg(column="category_id",aggfunc=assign_name)
    )
    return sku_per_catagroy

def get_products():
    path = "./products.csv" 
    product_data = pd.read_csv(path)
    return product_data