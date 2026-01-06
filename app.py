"""
Main Streamlit application.

This app provides an interactive exploration of the SEA-AD Alzheimer’s disease dataset,
including donor demographics and brain pathology measurements.
"""
import streamlit as st
import pandas as pd
from utils.io import load_data, load_csv
from sections import overview, brain_pathology

st.set_page_config(page_title="Exploring how Alzheimer’s disease impacts brain pathology and cognition across donors", layout="wide")

# --- 1. Load and Prepare Data (Cached) ---

donor_df = load_data()
mtg_df = load_csv()
# ---------- menu 

# --- 2. Sidebar / Filters ---
with st.sidebar:
    
    PAGES = {
        "Dashboard Overview": overview,
        "Brain pathology (MTG)": brain_pathology,
    }
    
    st.header("Navigation")
    selection = st.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
        
# --- 3. Render selected page ---
if selection == "Dashboard Overview":
    page.app(donor_df)
elif selection == "Brain pathology (MTG)":
    page.app(mtg_df)