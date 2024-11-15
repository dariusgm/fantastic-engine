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
    if selected_column in categorical:
        query = f"SELECT {selected_column}, COUNT(*) as CNT FROM {table_name} GROUP BY {selected_column}"
        result = con.execute(query).fetchdf()
        st.dataframe(result)
    elif selected_column in numerical:
        query = (f"SELECT "
                 f"AVG({selected_column}) as avg, "
                 f"MIN({selected_column}) as min, "
                 f"MAX({selected_column}) as max "
                 f"FROM {table_name}")
        result = con.execute(query).fetchdf()
        st.dataframe(result)



