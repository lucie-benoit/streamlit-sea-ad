"""
Utility functions for data loading and preprocessing.

This module handles:
- loading donor metadata from Excel files
- loading MTG pathology data from CSV files
- basic data cleaning and error handling
"""

import streamlit as st
import pandas as pd
from utils.prep import clean_data

def load_data(path='data/donor_metadata.xlsx'):
    """
    Load donor metadata from an Excel file and perform basic cleaning.

    Parameters
    ----------
    path : str
        Path to the donor metadata Excel file.

    Returns
    -------
    pd.DataFrame
        Cleaned donor metadata dataframe. Returns an empty dataframe if loading fails.
    """
    try:
        df = pd.read_excel(path)
        df = clean_data(df)
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()
    
def load_csv(path='data/all_mtg.csv'):
    """
    Load MTG pathology measurements from a CSV file.

    Parameters
    ----------
    path : str
        Path to the MTG pathology CSV file.

    Returns
    -------
    pd.DataFrame
        MTG pathology dataframe. Returns an empty dataframe if loading fails.
    """
     
    try:
        df = pd.read_csv(path)
        return df 
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()