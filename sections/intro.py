"""Hook, context, questions and dataset presentation."""

import streamlit as st

from utils.io import LICENSE_TEXT
from utils.refs import reference


def render_intro() -> None:
    st.title("How are the French doing ?")
    st.divider()
    st.subheader("Mental health became a major public-health issue over the past decade.")
    st.subheader("The WHO estimated that the first year of COVID-19 raised global anxiety and depression prevalence by 25% [1].")
    st.subheader("In France, the depressive-episode rate among 18–75 year-olds rose from 9.8% in 2017 to 13.3% in 2021, with the largest increase among 18–24 year-olds [2].")

    reference(1)
    reference(2)

    st.divider()
    st.subheader("How are these challenges reflected in actual pharmacy dispensing data ?")
    st.subheader("How prescription patterns changed since 2016 (taking into account the 2019-2020 crisis) ?")
    st.subheader("Who is the most affected among the French population ?")
    st.divider()
    st.subheader("Dataset presentation")
    st.text("The original datasets are from Open Medic (Assurance Maladie), recording reimbursed medicines dispensed in pharmacies across 2016, 2019 and 2025.Numeral price and general data about the patients (region, age and gender) were also given")
    st.text("Only psychotropic drugs (ATC coding) were kept and grouped by classes: benzodiazepines, Z-drugs, antidepressants, antipsychotics and lithium.")
    st.text("Only relevant dimensions (age, ATC label, region, gender, box quantity and year) were merged and cleaned.")
    st.caption(LICENSE_TEXT)


def render_dataset_overview(df) -> None:
    """Preview of the final table + definition of psychotropic drugs."""
    st.divider()
    st.write("Final dataset overview : ")
    st.dataframe(df.head(), hide_index=True)
    st.markdown("---")
    with st.expander("What are psychotropic drugs ?"):
        st.markdown("#### General definitions and classification ")
        st.write("Psychotropic medications are used to treat mental health disorders. Many psychotropic medications work by adjusting the number of major chemicals in the brain. These chemicals are called neurotransmitters. Increasing or decreasing certain neurotransmitters can counter the effects of certain mental health disorders.")
        st.write("""
    - **Antidepressants** : Often used to treat depression and anxiety. There are many different types that affect various neurotransmitter.
    - **Anxiolytics and Hypnotics** : Relieve anxiety and sleep disorders, often including benzodiazepines (e.g., alprazolam, zolpidem)
    - **Z-drugs** : target insomnia (Zolpidem, Zopiclone)
    - **Antipsychotics** : Manage symptoms of psychosis (eg. schizophrenia, bipolar 1 ...).
    - **Lithium** : Lithium is a type of mood stabilizer often used for bipolar disorder. There are others mood stabilizers but those are classified as epilepsy meds.
    """)
        st.write("Sometimes stimulants can be added to this list, it depends on the country classification")
        st.write("Keep in mind that psychotropic medications are not always a cure, they also can be more effective when associated with psychotherapy / counselling ")
        st.caption("Source: WebMD - What Are Psychotropic Medications?")
