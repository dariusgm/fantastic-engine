import streamlit as st
import pandas as pd
import duckdb
import os
import glob

def get_files(suffix = '*.csv'):
    return glob.glob(os.path.join("data", suffix), recursive=True)

def process_csv():
    csv_files = get_files("*.csv")
    csv_file = st.selectbox("Select a CSV file", csv_files)
    if st.button("Register Table", key="register_table"):
        df = pd.read_csv(csv_file)
        table_name = csv_file.split(os.sep)[-1].replace(".csv", "")
        with duckdb.connect("database.duckdb", read_only=False) as con:
            con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
            result = con.execute(f"SELECT COUNT(*) as CNT FROM {table_name}").fetchone()
            for r in result:
                st.write(f"Table {table_name} has {r} rows.")

def process_jsonl():
    jsonl_files = get_files("*.jsonl")
    jsonl_file = st.selectbox("Select a JSONL file", jsonl_files)
    if st.button("Register Table", key="register_table"):
        df = pd.read_json(jsonl_file, lines=True)
        table_name = jsonl_file.split(os.sep)[-1].replace(".jsonl", "")
        with duckdb.connect("database.duckdb", read_only=False) as con:
            con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
            result = con.execute(f"SELECT COUNT(*) as CNT FROM {table_name}").fetchone()
            for r in result:
                st.write(f"Table {table_name} has {r} rows.")

def process_json():
    json_files = get_files("*.json")
    json_file = st.selectbox("Select a JSON file", json_files)
    if st.button("Register Table", key="register_table"):
        df = pd.read_json(json_file, lines=False)
        table_name = json_file.split(os.sep)[-1].replace(".json", "")
        with duckdb.connect("database.duckdb", read_only=False) as con:
            con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
            result = con.execute(f"SELECT COUNT(*) as CNT FROM {table_name}").fetchone()
            for r in result:
                st.write(f"Table {table_name} has {r} rows.")

st.write("Hello World!")
all_data_sources = ["CSV [Comma Separated Values]", "JSONL [JSON Lines]", "JSON [JavaScript Object Notation]"]

data_source = st.selectbox("Select a Source", all_data_sources, key="source")
source = data_source.split(" ")[0]
if "CSV" == source:
    process_csv()
elif "JSONL" == source:
    process_jsonl()
elif "JSON" == source:
    process_json()
else:
    st.write("Unsupported data source")