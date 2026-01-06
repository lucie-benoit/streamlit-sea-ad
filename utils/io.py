# load_data(), fetch_and_cache(), license text
import streamlit as st
import pandas as pd
from utils.prep import clean_data

def load_data(path='data/donor_metadata.xlsx'):
    """
    Charge le fichier Excel et nettoie les colonnes numériques.
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
    
    """
    try:
        df = pd.read_csv(path)
        return df 
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()