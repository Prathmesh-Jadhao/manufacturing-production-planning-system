import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


@st.cache_data(ttl=60)
def fetch_data(endpoint: str) -> list:
    """Fetch data from the API with caching and error handling."""
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Unable to fetch {endpoint}: {e}")
        return []


def run_action(endpoint: str) -> dict | None:
    """Trigger a POST action on the API."""
    try:
        response = requests.post(f"{API_URL}{endpoint}", timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error running action {endpoint}: {e}")
        return None
