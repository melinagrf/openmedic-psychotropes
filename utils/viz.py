"""Chart functions: one place so every chart shares the same style."""

import altair as alt
import pandas as pd
import streamlit as st

from utils.constants import GENDER_COLORS, PASTEL_PALETTE


def class_bar_chart(df_overview: pd.DataFrame) -> None:
    """Section 1 - boxes dispensed per class and year (grouped bars)."""
    st.bar_chart(
        df_overview,
        x="annee",
        y="boites",
        color="classe",
        stack=False,
        x_label="Year",
        y_label="Boxes dispensed",
    )


def pct_change_line(df_melted: pd.DataFrame, years: list, base_year) -> alt.Chart:
    """Section 2 - evolution (%) of each class relative to the first selected year."""
    return (
        alt.Chart(df_melted)
        .mark_line(point=True, strokeWidth=2)
        .encode(
            x=alt.X("annee:O", title="Year", axis=alt.Axis(values=years)),
            y=alt.Y("pct_change:Q", title=f"% vs {base_year}"),
            color=alt.Color("classe:N", title="Drug Class", scale=alt.Scale(range=PASTEL_PALETTE)),
            tooltip=["annee", "classe", alt.Tooltip("pct_change:Q", format=".1f")],
        )
        .properties(height=400)
        .interactive()
    )


def molecule_change_bar(top: pd.Series, color: str, first_year, last_year) -> None:
    """Section 3 - change in boxes dispensed per molecule between two years."""
    st.bar_chart(top, horizontal=True, color=color)
    st.caption(f"Change in boxes dispensed ({first_year} vs {last_year}).")


def age_gender_chart(df_demo: pd.DataFrame) -> alt.Chart:
    """Section 4 - boxes by age group and gender, one panel per year."""
    return (
        alt.Chart(df_demo)
        .mark_bar()
        .encode(
            x=alt.X("age:N", title="Age Group"),
            y=alt.Y("boites:Q", title="Total Boxes Dispensed"),
            color=alt.Color("sexe:N", title="Gender", scale=alt.Scale(range=GENDER_COLORS)),
            column="annee:N",
            tooltip=["age", "sexe", "annee", "boites"],
        )
        .properties(width=180, height=300)
    )


def molecule_heatmap(df_heat: pd.DataFrame) -> alt.Chart:
    """Section 6 - boxes dispensed for the 15 most dispensed molecules, by year."""
    return (
        alt.Chart(df_heat)
        .mark_rect()
        .encode(
            x=alt.X("annee:O", title="Year"),
            y=alt.Y("atc_label:N", title="Molecule", sort="-x"),
            color=alt.Color("boites:Q", title="Boxes Dispensed", scale=alt.Scale(scheme="purples")),
            tooltip=["atc_label", "annee", "boites"],
        )
        .properties(height=400)
    )
