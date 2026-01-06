import pandas as pd
import streamlit as st

# utils/prep.py
# Avoid load_csv import to avoid circular import

def clean_data(df):
    """Clean the Fresh Brain Weight clolumn to convert it into numerical"""
    
    if "Fresh Brain Weight" in df.columns:
        # Replace "Unavailable" by NaN
        df["Fresh Brain Weight"] = pd.to_numeric(df["Fresh Brain Weight"], errors='coerce')
    return df 

def filtered(df_pathology):
    """
    Merge MTG pathology measurements with donor metadata and create derived variables.

    Returns
    -------
    pd.DataFrame
        Merged dataframe containing:
        - pathology markers (numeric)
        - Cognitive Status
        - ADNC (renamed from 'Overall AD neuropathological Change')
        - Dementia_status (categorical)
    """
    
    # ================= Load metadata =================
    df_meta = pd.read_excel("data/donor_metadata.xlsx")

    # ================= Select pathology columns =================
    pathology_cols = [
        "Donor ID",

        # Tau (AT8)
        "percent AT8 positive area_Grey matter",

        # Abeta
        "percent 6e10 positive area_Grey matter",

        # pTDP43
        "percent pTDP43 positive area_Grey matter",

        # aSyn
        "percent aSyn positive area_Grey matter",

        # Neurons
        "number of NeuN positive cells per area_Grey matter",

        # Microglia / Astrocytes
        "percent Iba1 positive area_Grey matter",
        "percent GFAP positive area_Grey matter",
    ]

    # --- Check missing pathology columns (important) ---
    missing_cols = [c for c in pathology_cols if c not in df_pathology.columns]
    if missing_cols:
        st.error("Missing pathology columns:")
        st.write(missing_cols)
        st.write("Available columns:", df_pathology.columns.tolist())
        return None

    df_patho = df_pathology[pathology_cols].copy()

    # ================= Select metadata columns =================
    meta_cols = ["Donor ID", "Cognitive Status", "Overall AD neuropathological Change"]
    missing_meta = [c for c in meta_cols if c not in df_meta.columns]
    if missing_meta:
        st.error("Missing metadata columns:")
        st.write(missing_meta)
        st.write("Available metadata columns:", df_meta.columns.tolist())
        return None

    df_meta = df_meta[meta_cols].copy()

    # ================= Create Dementia variable =================
    df_meta["Dementia"] = (
        df_meta["Cognitive Status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .apply(lambda x: ("dementia" in x) and ("no dementia" not in x))
    )

    df_meta["Dementia_status"] = df_meta["Dementia"].map(
        {True: "Dementia", False: "No dementia"}
    )   
    # ================= Merge =================
    df_merged = df_patho.merge(df_meta, on="Donor ID", how="inner")

    # ================= Final cleaning =================
    # Ensure numeric columns are numeric
    for col in pathology_cols[1:]:
        df_merged[col] = pd.to_numeric(df_merged[col], errors="coerce")

    return df_merged
