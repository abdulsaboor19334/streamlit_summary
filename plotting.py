import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_order_per_day(mtd,main):
    fig,ax = plt.subplots(2,1,figsize=(15, 15))

    mtd_group = mtd.groupby(mtd.date.dt.date).agg(
        total = pd.NamedAgg(column="shop_total",aggfunc="count")
    )

    main_group =main.groupby(main.date.dt.date).agg(
        total = pd.NamedAgg(column="shop_total",aggfunc="count")
    )
    plt.xticks(fontsize=25)
    plt.rcParams.update({'font.size': 25})

    sns.lineplot(mtd_group,ax=ax[0]).set(title="Order/day MTD")
    sns.lineplot(main_group,ax=ax[1]).set(title="Order/day since inception")

    ax[0].tick_params(labelsize=16, labelrotation=45)
    ax[1].tick_params(labelsize=16, labelrotation=45)

    fig.tight_layout()
    return fig

def top_10_category_by_sale(df):
    category_wise_sale = df.groupby("category_id",as_index=False).agg(
        total_count = pd.NamedAgg(column="shop_total",aggfunc="count"),
        total_sale = pd.NamedAgg(column="shop_total",aggfunc="sum"),
        total_quantity = pd.NamedAgg(column="quantity",aggfunc="sum"),
        category_name = pd.NamedAgg(column="category_name",aggfunc="first")
    )
    return category_wise_sale.sort_values("total_sale",ascending=False).head(10)

def top_10_products_by_sale(df):
    product_wise_sale = df.groupby("sku",as_index=False).agg(
        total_count = pd.NamedAgg(column="shop_total",aggfunc="count"),
        total_sale = pd.NamedAgg(column="shop_total",aggfunc="sum"),
        total_quantity = pd.NamedAgg(column="quantity",aggfunc="sum"),
        name = pd.NamedAgg(column="name",aggfunc="first")
    )
    return product_wise_sale.sort_values("total_sale",ascending=False).head(10)

def top_10_category_by_quantity(df):
    category_wise_sale = df.groupby("category_id",as_index=False).agg(
        total_count = pd.NamedAgg(column="shop_total",aggfunc="count"),
        total_sale = pd.NamedAgg(column="shop_total",aggfunc="sum"),
        total_quantity = pd.NamedAgg(column="quantity",aggfunc="sum"),
        category_name = pd.NamedAgg(column="category_name",aggfunc="first")
    )
    return category_wise_sale.sort_values("total_quantity",ascending=False).head(10)

def top_10_products_by_quantity(df):
    product_wise = df.groupby("sku",as_index=False).agg(
        total_count = pd.NamedAgg(column="shop_total",aggfunc="count"),
        total_sale = pd.NamedAgg(column="shop_total",aggfunc="sum"),
        total_quantity = pd.NamedAgg(column="quantity",aggfunc="sum"),
        name = pd.NamedAgg(column="name",aggfunc="first")
    )
    return product_wise.sort_values("total_quantity",ascending=False).head(10)

def sales_per_category(df):
    category_wise_sale = df.groupby("category_id",as_index=False).agg(
        total_count = pd.NamedAgg(column="shop_total",aggfunc="count"),
        total_sale = pd.NamedAgg(column="shop_total",aggfunc="sum"),
        total_quantity = pd.NamedAgg(column="quantity",aggfunc="sum"),
        category_name = pd.NamedAgg(column="category_name",aggfunc="first")
    )
    plt.figure(figsize=(22, 15))
    plt.rcParams.update({'font.size': 25})
    ax = sns.barplot(data=category_wise_sale,y="category_name",x="total_sale")
    fig = ax.get_figure()
    ax.tick_params(labelsize=25, labelrotation=42)
    return fig

def sales_per_product(df):
    products = top_10_products_by_sale(df)
    plt.figure(figsize=(22, 15))
    plt.rcParams.update({'font.size': 25})
    ax = sns.barplot(data=products,y="name",x="total_sale")
    fig = ax.get_figure()
    ax.tick_params(labelsize=25, labelrotation=42)
    return fig

def quantity_per_category(df):
    category_wise_sale = df.groupby("category_id",as_index=False).agg(
        total_count = pd.NamedAgg(column="shop_total",aggfunc="count"),
        total_sale = pd.NamedAgg(column="shop_total",aggfunc="sum"),
        total_quantity = pd.NamedAgg(column="quantity",aggfunc="sum"),
        category_name = pd.NamedAgg(column="category_name",aggfunc="first")
    )
    plt.figure(figsize=(22, 15))
    plt.rcParams.update({'font.size': 25})
    ax = sns.barplot(data=category_wise_sale,y="category_name",x="total_quantity")
    fig = ax.get_figure()
    ax.tick_params(labelsize=25, labelrotation=42)
    return fig

def quantity_per_product(df):
    products = top_10_products_by_quantity(df)
    plt.figure(figsize=(22, 15))
    plt.rcParams.update({'font.size': 25})
    ax = sns.barplot(data=products,y="name",x="total_quantity")
    fig = ax.get_figure()
    ax.tick_params(labelsize=25, labelrotation=42)
    return fig