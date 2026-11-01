# -*- coding: utf-8 -*-
"""How are the French doing ? - Streamlit data-storytelling app on Open Medic (psychotropic drugs).

Run from the project folder:
    python -m streamlit run app.py
"""

import streamlit as st

st.set_page_config(page_title="How are the French doing ?", layout="wide")

from sections.conclusions import render_conclusions  # noqa: E402
from sections.deep_dives import (  # noqa: E402
    render_demographics,
    render_heatmap,
    render_molecules,
    render_regions,
)
from sections.intro import render_dataset_overview, render_intro  # noqa: E402
from sections.overview import render_kpis, render_overview  # noqa: E402
from sections.quality import render_quality  # noqa: E402
from sections.sidebar import render_sidebar  # noqa: E402
from utils.io import DATA_PATH, load_data  # noqa: E402
from utils.prep import apply_filters  # noqa: E402

if not DATA_PATH.exists():
    st.error(
        f"Data file not found: `{DATA_PATH}`. "
        "Copy `openmedic_psychotropes.csv` into the `data/` folder (see README.md, section Data)."
    )
    st.stop()

df = load_data()

# Story: hook -> data quality -> filters/KPIs -> analyses -> conclusions
render_intro()
render_quality(df)
render_dataset_overview(df)

regions, years, classes, years_list = render_sidebar(df)
df_filtered = apply_filters(df, regions, years, classes)

render_kpis(df_filtered, years_list, years)
render_overview(df_filtered)
render_molecules(df)
render_demographics(df, df_filtered)
render_regions(df_filtered)
render_heatmap(df_filtered)
render_conclusions()
