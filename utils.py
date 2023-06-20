import streamlit as st

def print_aov(df):
  gross_sale = df["shop_total"]
  gross_aov = round(gross_sale.sum()/len(df),2)
  return gross_aov

def print_sales(df):
  gross_sale = df["shop_total"]
  return '{:,}'.format(gross_sale.sum())

