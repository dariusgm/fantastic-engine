import streamlit as st
import pandas as pd
import duckdb
import os
import glob


with duckdb.connect("database.duckdb", read_only=True) as con:
    query = "SELECT table_name FROM information_schema.tables"
    st.code(body=query, language="sql")
    # Execute the query and fetch the results
    tables = con.execute(query).fetchdf()

    options = tables['table_name'].tolist()

    table_name = st.selectbox("Select a Table", options, key="table")
    select_query = f"SELECT * FROM '{table_name}' LIMIT 100"
    st.code(body=select_query, language="sql")
    result = con.execute(select_query).fetchdf()
    st.dataframe(result, key="query_result")


    # Query to get table types
    query = f"""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = '{table_name}'
    """

    # Execute the query and fetch the results
    table_types = con.execute(query).fetchall()
    categorical = []
    numerical = []
    for row in table_types:
        column_name, column_type = row
        if column_type in ["INTEGER", "FLOAT", "BIGINT", "DOUBLE"]:
            numerical.append(column_name)
        else:
            categorical.append(column_name)

    # Print the results
    type_map = {}
    for c in categorical:
        type_map[c] = f" {c} [Categorical]"

    for n in numerical:
        type_map[n] = f" {n} [Numerical]"

    def get_type_map(x):
        return type_map[x]

    selected_column = st.selectbox("Select a column", numerical + categorical, key="column", format_func=get_type_map)
    st.write(f"Selected column: {selected_column}")
    st.write(f"Column type: {column_type}")



