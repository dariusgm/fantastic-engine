import streamlit as st
import pandas as pd
import duckdb
import os

st.write("Hello World!")

source = st.selectbox("Select a Source", ["CSV"], key="source")


if source == "CSV":
    csv_file = st.selectbox("Select a CSV file", ["data_Q1_2024/2024-01-01.csv", "example.csv"])
    df = pd.read_csv(csv_file)
    table_name = csv_file.split(os.sep)[-1].replace(".csv", "")
    with duckdb.connect("database.duckdb") as con:
        con.register(table_name, df)
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
        if selected_column in numerical:
            st.write(f"Min: {result[selected_column].min()}")
            st.write(f"Mean: {result[selected_column].mean()}")
            st.write(f"Median: {result[selected_column].median()}")
            st.write(f"Standard Deviation: {result[selected_column].std()}")
            st.write(f"Max: {result[selected_column].max()}")
        else:
            st.write(f"Value Counts: {result[selected_column].value_counts()}")





