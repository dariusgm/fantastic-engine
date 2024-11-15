import streamlit as st
import pandas as pd
import duckdb
import os
import glob

@st.cache_resource
def get_database():
    return duckdb.connect("database.duckdb", read_only=False)

def get_csv_files():
    return glob.glob(os.path.join("data", "*.csv"), recursive=True)

st.write("Hello and welcome to fantastic-engine!")
