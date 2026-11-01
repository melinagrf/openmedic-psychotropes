"""Data loading. The app reads one prepared table: data/openmedic_psychotropes.csv."""

from pathlib import Path

import pandas as pd
import streamlit as st

from utils.constants import (
    AGE_TRANSLATION,
    CLASS_TRANSLATION,
    GENDER_TRANSLATION,
    OVERSEAS_CODE,
    OVERSEAS_LABEL,
    REGION_NAMES,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "openmedic_psychotropes.csv"

LICENSE_TEXT = "Sources: Open Medic 2025, 2019, 2016 — CNAM / data.gouv.fr — Open Licence"


@st.cache_data(show_spinner="Loading data...")
def load_data(path: str = str(DATA_PATH)) -> pd.DataFrame:
    """Read the merged Open Medic psychotropics table and translate its labels to English."""
    df = pd.read_csv(path)
    df["region_code"] = (
        df["region_code"].astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(2)
    )
    # Official (accented) region names from the codes; code 5 = overseas, flagged explicitly
    df["region"] = df["region_code"].map(REGION_NAMES).fillna(df["region"])
    df.loc[df["region_code"] == OVERSEAS_CODE, "region"] = OVERSEAS_LABEL
    df["classe"] = df["classe"].replace(CLASS_TRANSLATION)
    df["sexe"] = df["sexe"].replace(GENDER_TRANSLATION)
    df["age"] = df["age"].replace(AGE_TRANSLATION)
    return df
