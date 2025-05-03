import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

st.title("🔍 Duplicate & Similar Data Finder")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
threshold = st.slider("Set Similarity Threshold", 70, 100, 90)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Original Data", df.head())

    column = st.selectbox("Select column to check for duplicates", df.columns)
    
    similar_pairs = []
    checked = set()

    for i, val1 in enumerate(df[column]):
        for j, val2 in enumerate(df[column]):
            if i >= j or (i, j) in checked or pd.isna(val1) or pd.isna(val2):
                continue
            similarity = fuzz.token_sort_ratio(str(val1), str(val2))
            if similarity >= threshold:
                similar_pairs.append((val1, val2, similarity))
            checked.add((i, j))

    if similar_pairs:
        st.write(f"🔍 Found {len(similar_pairs)} similar entries:")
        sim_df = pd.DataFrame(similar_pairs, columns=["Value 1", "Value 2", "Similarity"])
        st.dataframe(sim_df)
    else:
        st.write("✅ No similar data found based on the given threshold.")
