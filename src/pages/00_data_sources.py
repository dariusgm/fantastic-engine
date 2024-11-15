import streamlit as st
import pandas as pd
import duckdb
import os
import glob

from main import get_database


def get_csv_files():
    return glob.glob(os.path.join("data", "*.csv"), recursive=True)

st.write("Hello World!")
source = st.selectbox("Select a Source", ["CSV"], key="source")

if source == "CSV":
    csv_files = get_csv_files()
    csv_file = st.selectbox("Select a CSV file", csv_files)
    if st.button("Register Table", key="register_table"):
        df = pd.read_csv(csv_file)
        table_name = csv_file.split(os.sep)[-1].replace(".csv", "")
        with duckdb.connect("database.duckdb", read_only=False) as con:
            con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
            result = con.execute(f"SELECT COUNT(*) as CNT FROM {table_name}").fetchone()
            for r in result:
                st.write(f"Table {table_name} has {r} rows.")