import streamlit as st
from supabase import Client,create_client
supabase: Client=create_client(
    st.secrets["supabase_url"],
    st.secrets["supabase_key"]
)