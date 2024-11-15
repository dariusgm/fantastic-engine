import streamlit as st
import pandas as pd
import duckdb
import os
import glob


def get_csv_files():
    return glob.glob(os.path.join("data", "*.csv"), recursive=True)

st.write("Hello and welcome to fantastic-engine!")
