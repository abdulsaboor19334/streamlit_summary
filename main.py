import streamlit as st
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from clean import clean
from fetch_skus import get_skus
from utils import print_aov, print_sales
from plotting import plot_order_per_day, sales_per_category, top_10_by_sale,top_10_by_quantity,quantity_per_category

file = st.file_uploader(
    label="Hub Sale File",
    type=["csv","xlsx","xls"],
    key="file_uploader",
    help="upload a single or multiple sales files from hubs"
    )

if file != None:
    csv = clean(pd.read_csv(file))

    sku = get_skus()

    main = csv.merge(sku,left_on="sku_code",right_on="sku",how="left")
    mtd = main.loc[(main.date.dt.month == datetime.date.today().month)&(main.date.dt.year == datetime.date.today().year)]

    column_1,column_2 = st.columns(2)

    column_1.metric("AOV MTD",print_aov(mtd))
    column_2.metric("AOV Total",print_aov(main))
    column_1.metric("Sales MTD", print_sales(mtd))
    column_2.metric("Sales Total", print_sales(main))
    column_1.metric("SKUs Sold MTD", len(mtd))
    column_2.metric("SKU Sold Total", len(main))

    st.markdown("## Top 10 by Sales MTD")
    top_10 = top_10_by_sale(mtd)
    st.write(top_10)
    
    st.markdown("## Top 10 by Quantity MTD")
    top_10_quantity = top_10_by_quantity(mtd)
    st.write(top_10_quantity)

    st.markdown("## Top 10 by Sales Total")
    top_10 = top_10_by_sale(main)
    st.write(top_10)
    
    st.markdown("## Top 10 by Quantity Total")
    top_10_quantity = top_10_by_quantity(main)
    st.write(top_10_quantity)

    st.pyplot(plot_order_per_day(mtd,main),clear_figure=True)
    
    st.markdown("## Sales/Category")
    st.pyplot(sales_per_category(mtd))

    st.markdown("## Quantity/Category")
    st.pyplot(quantity_per_category(mtd))