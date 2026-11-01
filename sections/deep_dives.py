"""Sections 3 to 6: molecules, demographics, regions, heatmap."""

import streamlit as st

from utils.constants import (
    ANTIDEPRESSANT_CLASSES,
    ANTIPSYCHOTIC_CLASSES,
    BENZODIAZEPINE_CLASSES,
    COLOR_ANTIDEPRESSANTS,
    COLOR_ANTIPSYCHOTICS,
    COLOR_BENZODIAZEPINES,
    UNKNOWN,
)
from utils.prep import molecule_change, regional_rates
from utils.refs import reference
from utils.viz import age_gender_chart, molecule_change_bar, molecule_heatmap


def _molecule_block(df, classes, first_year, last_year, slider_label, slider_max, key, color, name) -> None:
    """Slider + horizontal bar chart of the change per molecule for one family of drugs."""
    n_top = st.slider(slider_label, 3, slider_max, slider_max, key=key)
    # Computed on the full table so that a sidebar filter never empties the chart
    top, state = molecule_change(df, classes, first_year, last_year, n_top)
    if state == "ok":
        molecule_change_bar(top, color, first_year, last_year)
    elif state == "no_years":
        st.info(f"Insufficient yearly columns for {name} comparison.")
    else:
        st.info(f"No {name} data found.")


def render_molecules(df) -> None:
    """Section 3 - which medicines drive the change?"""
    st.header("3 - Which medicines drive the change?")
    st.text("Analysis for the main classes: antidepressants, antipsychotics, and benzodiazepines.")

    all_years = sorted(df["annee"].unique())
    first_year, last_year = all_years[0], all_years[-1]

    st.subheader("Among antidepressants")
    _molecule_block(df, ANTIDEPRESSANT_CLASSES, first_year, last_year,
                    "Antidepressant molecules shown", 10, "s_antidep", COLOR_ANTIDEPRESSANTS, "antidepressant")
    st.write("The antidepressants growth comes mainly from sertraline, paroxetine and fluoxetine. Citalopram and escitalopram slightly decline.")
    st.write("The rise is therefore concentrated in a few molecules rather than being general.")

    st.subheader("Among antipsychotics")
    _molecule_block(df, ANTIPSYCHOTIC_CLASSES, first_year, last_year,
                    "Antipsychotic molecules shown", 10, "s_antipsy", COLOR_ANTIPSYCHOTICS, "antipsychotic")
    st.write("Quetiapine and Aripiprazole lead the increase.")
    st.write("This might be linked to the increase of off-label uses [6], which means that antipsychotics may be prescribed for other symptoms (not officially approved) when first-use treatments are not successful.")
    reference(6)

    st.subheader("Among benzodiazepines")
    _molecule_block(df, BENZODIAZEPINE_CLASSES, first_year, last_year,
                    "Benzodiazepine molecules shown", 6, "s_benzo", COLOR_BENZODIAZEPINES, "benzodiazepine")
    st.write("Oxazepam and diazepam rise, while bromazepam, lorazepam and clorazepate fall, which suggests substitution between molecules rather than a simple decline.")


def render_demographics(df, df_filtered) -> None:
    """Section 4 - who is concerned?"""
    st.header("4 - Who is concerned?")
    st.subheader("Age & Gender Breakdown")

    demo_class = st.selectbox("Select drug class for demographics", sorted(df["classe"].unique()), key="demo_class")
    df_demo = df_filtered[
        (df_filtered["classe"] == demo_class)
        & (df_filtered["age"] != UNKNOWN)
        & (df_filtered["sexe"] != UNKNOWN)
    ]
    df_demo = df_demo.groupby(["age", "sexe", "annee"], as_index=False)["boites"].sum()

    if not df_demo.empty:
        st.altair_chart(age_gender_chart(df_demo))
        st.caption(f"Comparison across age groups and genders for {demo_class}.")

    st.write("Women receive about two thirds of antidepressant boxes (no matter their age ranges and the year). Women are the groups with the highest depressive-episode rates in 2021 [1]. Some scientists are investigating whether it is linked to a possible gender bias [7].")
    st.write("HCFEA reports +62.6% in antidepressant consumption among under-18s between 2014 and 2021 [8].")

    reference(1)
    reference(7)
    reference(8)


def render_regions(df_filtered) -> None:
    """Section 5 - top 5 regions per 1,000 inhabitants, one map + table per year."""
    st.header("5 - Top 5 regions by consumption per 1,000 inhabitants")
    st.caption("Maps and tables show the Top 5 regions adjusted for population size (boxes dispensed per 1,000 inhabitants).")

    years_reg = sorted(df_filtered.loc[df_filtered["region"] != UNKNOWN, "annee"].unique())
    if years_reg:
        cols = st.columns(len(years_reg))
        for col, year in zip(cols, years_reg):
            with col:
                st.subheader(f"Year {year}")
                top5 = regional_rates(df_filtered, year)

                map_data = top5.dropna(subset=["lat", "lon"]).copy()
                if not map_data.empty:
                    max_val = max(map_data["conso_1000hab"].max(), 1e-9)
                    map_data["size"] = 20000 + (map_data["conso_1000hab"] / max_val) * 50000
                    map_data["color"] = "#A27CA2C0"
                    st.map(map_data, latitude="lat", longitude="lon", size="size", color="color")

                st.write("**Top 5 (per 1,000 inhab.):**")
                st.dataframe(
                    top5[["region", "conso_1000hab"]].rename(
                        columns={"region": "Region", "conso_1000hab": "Boxes / 1k hab"}
                    ),
                    hide_index=True,
                )

    st.write("Bretagne has the highest rate in all three years, with Provence-Alpes-Côte d'Azur a close second. Normandie, Nouvelle-Aquitaine and Hauts-de-France complete the top 5, which is made of the same five regions in 2016, 2019 and 2025.")
    st.write("The ranking seems to be stable over time, regional differences are structural rather than a COVID effect. A departmental reporting could be more relevant.")
    st.write("It is however important to highlight that the DOM-TOM (french overseas departments and regions) are not properly included in the dataset: they are all grouped under region code 5 and cannot be analysed or mapped.")


def render_heatmap(df_filtered) -> None:
    """Section 6 - molecule heatmap."""
    st.header("6 - Molecule heatmap")
    st.subheader("Top prescribed molecules: trend heatmap")

    top_molecules = df_filtered.groupby("atc_label")["boites"].sum().nlargest(15).index
    df_heat = (
        df_filtered[df_filtered["atc_label"].isin(top_molecules)]
        .groupby(["atc_label", "annee"], as_index=False)["boites"]
        .sum()
    )
    if not df_heat.empty:
        st.altair_chart(molecule_heatmap(df_heat), width="stretch")

    st.write("The heatmap summarises the observations of part 3 : zolpidem and zopiclone fade, while sertraline, paroxetine, venlafaxine and oxazepam darken")
