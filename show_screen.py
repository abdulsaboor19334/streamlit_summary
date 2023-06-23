import streamlit as st
import datetime 
import pandas as pd
from base64 import b64encode
import os
from clean import clean
from fetch_skus import get_skus, get_products
from utils import print_aov, print_sales
from cryptography.hazmat.primitives import hashes
from plotting import (
    plot_order_per_day, 
    sales_per_category, 
    top_10_category_by_sale,
    top_10_category_by_quantity,
    quantity_per_category,
    top_10_products_by_quantity,
    plot_order_per_day_single,
    top_10_products_by_sale,
    sales_per_product,
    quantity_per_product
    )

def hubwise_sales(df):
    pass

def single_hub(file):
    csv = clean(pd.read_csv(file))

    sku = get_skus()
    products = get_products()

    main = csv.merge(sku,left_on="sku_code",right_on="sku",how="left").merge(products,on="sku",how='left')
    mtd = main.loc[(main.date.dt.month == datetime.date.today().month)&(main.date.dt.year == datetime.date.today().year)]

    column_1,column_2 = st.columns(2)

    column_1.metric("AOV MTD",print_aov(mtd))
    column_2.metric("AOV Total",print_aov(main))
    column_1.metric("Sales MTD", print_sales(mtd))
    column_2.metric("Sales Total", print_sales(main))
    column_1.metric("SKUs Sold MTD", len(mtd))
    column_2.metric("SKU Sold Total", len(main))

    st.markdown("## Top 10 SKUs by Sales MTD")
    top_10 = top_10_products_by_sale(mtd)
    st.write(top_10)

    st.markdown("## Top 10 Categories by Sales MTD")
    top_10 = top_10_category_by_sale(mtd)
    st.write(top_10)
    
    st.markdown("## Top 10 categories by Quantity MTD")
    top_10_quantity = top_10_category_by_quantity(mtd)
    st.write(top_10_quantity)

    st.markdown("## Top 10 SKUs by Quantity MTD")
    top_10_quantity = top_10_products_by_quantity(mtd)
    st.write(top_10_quantity)

    st.markdown("## Top 10 Categories by Sales Total")
    top_10 = top_10_category_by_sale(main)
    st.write(top_10)

    st.markdown("## Top 10 SKUs by Sales Total")
    top_10 = top_10_products_by_sale(main)
    st.write(top_10)
    
    st.markdown("## Top 10 categories by Quantity Total")
    top_10_quantity = top_10_category_by_quantity(main)
    st.write(top_10_quantity)

    st.markdown("## Top 10 SKUs by Quantity Total")
    top_10_quantity = top_10_products_by_quantity(main)
    st.write(top_10_quantity)

    st.pyplot(plot_order_per_day(mtd,main),clear_figure=True)
    
    st.markdown("## Sales/Category")
    st.pyplot(sales_per_category(mtd))

    st.markdown("## Quantity/Category")
    st.pyplot(quantity_per_category(mtd))

    st.markdown("## Sales/Top SKUs")
    st.pyplot(sales_per_product(mtd))

    st.markdown("## Quantity/Top SKU")
    st.pyplot(quantity_per_product(mtd))

def master_archive(df):
    csv = pd.read_csv(df)
    csv.columns = [col.lower().strip().replace(" ","_") for col in csv.columns]
    csv["date"] = pd.to_datetime(csv.date, format="%d/%m/%Y")
    csv = csv.loc[~csv["sku_name"].isna()]

    def assign_num(x):
        encode = b64encode(os.urandom(11)).decode('utf8')  
        return encode
    csv["order_number"] = csv.order_number.apply(assign_num)

    def rename(hub):
        if "abbas" in hub.lower():
            return "Abbas"
        elif "johar" in hub.lower():
            return "Johar"
        elif "buffer" in hub.lower():
            return "Buffer"
        elif "nagan" in hub.lower():
            return "Nagan"
        elif "anwar" in hub.lower():
            return "Anwar"

    csv["hub_name"] = csv.hub_name.apply(rename)
    
    sku = get_skus()
    products = get_products()

    main = csv.merge(sku,left_on="sku_id",right_on="sku",how="left").merge(products,on="sku",how='left')

    total_group = main.groupby("hub_name").agg(
        shop_total = pd.NamedAgg(column="shop_total",aggfunc="sum"),
        aov = pd.NamedAgg(column="shop_total",aggfunc="mean")
    ).sort_values("hub_name")

    st.metric("Total Sales",total_group.shop_total.sum())
    st.metric(
        "Aov derived",
        round(main.shop_total.sum()/len(main.order_number.unique())),
        help="This is the AOV which uses derived order numbers"
        )

    st.markdown("## Hub Wise Numbers total")
    st.write(total_group)

    st.markdown("## Top 10 Categories by Sales Total")
    top_10 = top_10_category_by_sale(main)
    st.write(top_10)

    st.markdown("## Top 10 SKUs by Sales Total")
    top_10 = top_10_products_by_sale(main)
    st.write(top_10)

    st.markdown("## Top 10 categories by Quantity Total")
    top_10_quantity = top_10_category_by_quantity(main)
    st.write(top_10_quantity)

    st.markdown("## Top 10 SKUs by Quantity Total")
    top_10_quantity = top_10_products_by_quantity(main)
    st.write(top_10_quantity)

    st.pyplot(plot_order_per_day_single(main),clear_figure=True)

    st.markdown("## Sales/Category")
    st.pyplot(sales_per_category(main))

    st.markdown("## Quantity/Category")
    st.pyplot(quantity_per_category(main))

    st.markdown("## Sales/Top SKUs")
    st.pyplot(sales_per_product(main))

    st.markdown("## Quantity/Top SKU")
    st.pyplot(quantity_per_product(main))