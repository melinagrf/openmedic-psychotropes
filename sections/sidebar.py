"""Sidebar filters."""

import streamlit as st

from utils.constants import UNKNOWN


def render_sidebar(df):
    """Draw the filters and return (regions, years, classes, years_list)."""
    with st.sidebar:
        st.header("Filters")

        regions_list = sorted([r for r in df["region"].unique() if r != UNKNOWN])
        selected_regions = st.multiselect("Region", options=regions_list, default=regions_list)

        years_list = sorted(df["annee"].unique())
        selected_years = st.multiselect("Year", options=years_list, default=years_list)

        classes_list = sorted(df["classe"].unique())
        selected_classes = st.multiselect("Drug Class", options=classes_list, default=classes_list)

    return selected_regions, selected_years, selected_classes, years_list
