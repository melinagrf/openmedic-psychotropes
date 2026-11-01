"""Data quality section: all figures are computed from the loaded table."""

import streamlit as st

from utils.prep import audit_quality, fmt_int, quality_table


def render_quality(df) -> None:
    audit = audit_quality(df)

    st.divider()
    st.header("Data Quality & Validation Controls")
    st.caption("Quantitative audit, missing value treatment, and integrity checks performed on the Open Medic datasets.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records Audited", fmt_int(audit["rows"]))
    c2.metric("Missing Values (NaN)", f"{audit['missing_total']}")
    c3.metric("Duplicate Rows", f"{audit['duplicates']}")
    c4.metric("Unmapped Regions ('Inconnu')", fmt_int(audit["unknown_region"]))

    left, _ = st.columns([1, 1])
    with left:
        st.dataframe(quality_table(audit), hide_index=True, width="stretch")

    num_status = "verified" if audit["numeric_ok"] else "NOT numeric - check the CSV"
    st.write(f"Types: {num_status} data types (annee as integer, categorical codes for region_code and numerical measures for boites and rem).")
    st.write(f"Logical sanity checks: {fmt_int(audit['negatives'])} negative value(s) found in box counts and reimbursements.")
    st.write("Handling unmapped categories: rows with unmapped region (Inconnu) are preserved in our dataset but excluded for maps.")
