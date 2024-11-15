import streamlit as st
import pandas as pd
import duckdb
import os
import glob

def get_files(suffix = '*.csv'):
    return glob.glob(os.path.join("data", suffix), recursive=True)

def create_table(con, table_name, df):
    con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
    result = con.execute(f"SELECT COUNT(*) as CNT FROM {table_name}").fetchone()
    for r in result:
        st.success(f"Table {table_name} created with {r} rows.")

def process(file_type):
    files = get_files(f"*.{file_type}")
    file = st.selectbox(f"Select a {file_type.upper()} file", files)
    if st.button("Register Table", key="register_table"):
        if "csv" == file_type:
            df = pd.read_csv(file)
        elif "jsonl" == file_type or "json" == file_type:
            is_jsonl = "jsonl" == file_type
            df = pd.read_json(file, lines=is_jsonl)
        else:
            st.error(f"Unsupported file type: {file_type}")
            return
        table_name = file.split(os.sep)[-1].replace(f".{file_type}", "")

        with duckdb.connect("database.duckdb", read_only=False) as con:
            query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
            result = con.execute(query).fetchone()
            with st.form(key="create_table"):
                if result[0] > 0:
                    st.write(f"Table {table_name} already exists. Overwrite?")
                    if st.form_submit_button("Overwrite Table!"):
                        con.execute(f"DROP TABLE {table_name}")
                        create_table(con, table_name, df)
                    else:
                        st.warning("Table not overwritten.")
                else:
                    create_table(con, table_name, df)


st.write("Hello World!")
all_data_sources = ["CSV [Comma Separated Values]", "JSONL [JSON Lines]", "JSON [JavaScript Object Notation]"]

data_source = st.selectbox("Select a Source", all_data_sources, key="source")
source = data_source.split(" ")[0]
process(source.lower())
