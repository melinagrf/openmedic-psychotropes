"""Cleaning checks, filtering and aggregation helpers."""

import pandas as pd
import streamlit as st

from utils.constants import CENTRES, OVERSEAS_CODE, POPULATION_BY_CODE, REGION_NAMES, UNKNOWN


def fmt_int(value) -> str:
    """12345678 -> '12 345 678'."""
    return f"{value:,.0f}".replace(",", " ")


@st.cache_data(show_spinner=False)
def audit_quality(df: pd.DataFrame) -> dict:
    """Compute the data-quality indicators displayed in the 'Data Quality' section."""
    n = len(df)
    pct = lambda k: (k / n * 100) if n else 0.0  # noqa: E731

    missing_total = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())
    missing_keys = int(df[["atc", "annee"]].isnull().sum().sum())
    unknown_region = int((df["region"] == UNKNOWN).sum())
    overseas = int((df["region_code"] == OVERSEAS_CODE).sum())
    unknown_age = int((df["age"] == UNKNOWN).sum())
    unknown_sex = int((df["sexe"] == UNKNOWN).sum())
    negatives = int((df[["boites", "rem"]] < 0).sum().sum())
    numeric_ok = all(pd.api.types.is_numeric_dtype(df[c]) for c in ["annee", "boites", "rem"])

    return {
        "rows": n,
        "missing_total": missing_total,
        "duplicates": duplicates,
        "missing_keys": missing_keys,
        "unknown_region": unknown_region,
        "overseas": overseas,
        "unknown_age": unknown_age,
        "unknown_sex": unknown_sex,
        "negatives": negatives,
        "numeric_ok": numeric_ok,
        "pct": {
            "duplicates": pct(duplicates),
            "missing_keys": pct(missing_keys),
            "unknown_region": pct(unknown_region),
            "overseas": pct(overseas),
            "unknown_age": pct(unknown_age),
            "unknown_sex": pct(unknown_sex),
            "negatives": pct(negatives),
        },
    }


def quality_table(audit: dict) -> pd.DataFrame:
    """Summary table of the integrity checks (status computed from the data, not hard-coded)."""
    p = audit["pct"]

    def status(count: int) -> str:
        return "ok" if count == 0 else "to review"

    unknown_age_sex = audit["unknown_age"] + audit["unknown_sex"]
    return pd.DataFrame(
        {
            "Metric / Check": [
                "Rows audited (merged 2016, 2019, 2025)",
                "Exact Duplicate Records",
                "Missing Values in Critical Keys (ATC / Year)",
                "Unresolved Region Identifiers ('Inconnu')",
                "Overseas region code 5 (not usable for maps)",
                "Unresolved Age Records ('Inconnu')",
                "Unresolved Gender Records ('Inconnu')",
                "Negative Box / Reimbursement Quantities",
            ],
            "Result": [
                fmt_int(audit["rows"]),
                f"{fmt_int(audit['duplicates'])} ({p['duplicates']:.2f}%)",
                f"{fmt_int(audit['missing_keys'])} ({p['missing_keys']:.2f}%)",
                f"{fmt_int(audit['unknown_region'])} ({p['unknown_region']:.2f}%)",
                f"{fmt_int(audit['overseas'])} ({p['overseas']:.2f}%)",
                f"{fmt_int(audit['unknown_age'])} ({p['unknown_age']:.2f}%)",
                f"{fmt_int(audit['unknown_sex'])} ({p['unknown_sex']:.2f}%)",
                f"{fmt_int(audit['negatives'])} ({p['negatives']:.2f}%)",
            ],
            "Status": [
                "ok",
                status(audit["duplicates"]),
                status(audit["missing_keys"]),
                status(audit["unknown_region"]),
                status(audit["overseas"]),
                status(audit["unknown_age"]),
                status(audit["unknown_sex"]),
                status(audit["negatives"]),
            ],
        }
    )


def apply_filters(df: pd.DataFrame, regions, years, classes) -> pd.DataFrame:
    """Filter the table with the sidebar selections."""
    mask = df["region"].isin(regions) & df["annee"].isin(years) & df["classe"].isin(classes)
    return df[mask].copy()


def kpis(df_filtered: pd.DataFrame, years_list, selected_years) -> dict:
    """Headline figures for the target year (latest selected) vs the reference year."""
    ref_year = 2016 if 2016 in years_list else (min(selected_years) if selected_years else 2016)
    target_year = max(selected_years) if selected_years else ref_year

    total_boxes = df_filtered.loc[df_filtered["annee"] == target_year, "boites"].sum()
    total_rem = df_filtered.loc[df_filtered["annee"] == target_year, "rem"].sum()
    boxes_ref = df_filtered.loc[df_filtered["annee"] == ref_year, "boites"].sum()

    return {
        "ref_year": ref_year,
        "target_year": target_year,
        "total_boxes": total_boxes,
        "total_rem": total_rem,
        "delta_pct": ((total_boxes - boxes_ref) / boxes_ref * 100) if boxes_ref > 0 else 0,
        "avg_cost": (total_rem / total_boxes) if total_boxes > 0 else 0,
    }


def molecule_change(df: pd.DataFrame, classes, first_year, last_year, n_top: int):
    """Change in boxes dispensed per molecule between two years (top n by absolute change)."""
    sub = df[df["classe"].isin(classes)]
    if sub.empty:
        return None, "empty"
    mol = sub.groupby(["atc_label", "annee"])["boites"].sum().unstack(fill_value=0)
    if first_year not in mol.columns or last_year not in mol.columns:
        return None, "no_years"
    change = mol[last_year] - mol[first_year]
    top = change.reindex(change.abs().nlargest(n_top).index).sort_values()
    return top, "ok"


def regional_rates(df_filtered: pd.DataFrame, year: int) -> pd.DataFrame:
    """Top 5 regions by boxes per 1,000 inhabitants for one year (with marker coordinates).

    Regions are matched on their code (names differ in accents between sources); rows without a
    population (unknown region, overseas code 5) are left out.
    """
    reg = (
        df_filtered[df_filtered["annee"] == year]
        .groupby("region_code", as_index=False)["boites"]
        .sum()
    )
    reg["population"] = reg["region_code"].map(POPULATION_BY_CODE)
    reg = reg.dropna(subset=["population"]).copy()
    reg["region"] = reg["region_code"].map(REGION_NAMES)
    reg["conso_1000hab"] = reg["boites"] / reg["population"] * 1000
    top5 = reg.nlargest(5, "conso_1000hab").copy()
    top5["lat"] = top5["region_code"].map(lambda c: CENTRES.get(c, (None, None))[0])
    top5["lon"] = top5["region_code"].map(lambda c: CENTRES.get(c, (None, None))[1])
    return top5
