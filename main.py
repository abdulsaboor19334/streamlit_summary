import streamlit as st
from show_screen import single_hub,master_archive
import pandas as pd
from clean import clean
st.set_page_config(layout="wide",page_title="Hub Sales Report Genrator")

with st.form("main_form",clear_on_submit=True):
    file = st.file_uploader(
        label="Hub Sale File",
        type=["csv","xlsx","xls"],
        key="file_uploader",
        help="upload a single or multiple sales files from hubs",
        )
    is_master = st.checkbox("master archive?")
    st.form_submit_button()

if file != None:
    if not is_master:
        single_hub(file)
    else:
        master_archive(file)
