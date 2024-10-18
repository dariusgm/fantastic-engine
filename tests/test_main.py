import pandas as pd
from streamlit.testing.v1 import AppTest


def test_main():
    at = AppTest("src/main.py", default_timeout=20)
    at.run(timeout=20)
    at.selectbox("source").select("CSV")
    dataframe_element = at.dataframe[0]
    dataframe_content = dataframe_element.value
    expected_dataframe = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [30, 25, 35],
        "city": ["New York", "Los Angeles", "Chicago"]})
    pd.testing.assert_frame_equal(left=dataframe_content, right=expected_dataframe, check_exact=True)

