"""KPIs, class overview (section 1) and relative evolution (section 2)."""

import streamlit as st

from utils.prep import fmt_int, kpis
from utils.refs import reference
from utils.viz import class_bar_chart, pct_change_line


def render_kpis(df_filtered, years_list, selected_years) -> None:
    k = kpis(df_filtered, years_list, selected_years)
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric(
        f"Total Boxes ({k['target_year']})",
        fmt_int(k["total_boxes"]),
        f"{k['delta_pct']:+.1f}% vs {k['ref_year']}",
    )
    c2.metric(f"Total Reimbursement ({k['target_year']})", f"{fmt_int(k['total_rem'])} €")
    c3.metric(f"Avg Cost per Box ({k['target_year']})", f"{k['avg_cost']:.2f} €")
    st.markdown("---")


def render_overview(df_filtered) -> None:
    # ---- 1 - Overview -------------------------------------------------------------
    st.header("1 - Overview : psychotropic drugs dispensing by classes")
    st.subheader("How much did dispensing change between selected years?")
    st.caption("Psychotropic drugs dispensing by classes in 2016, 2019 and 2025")

    df_overview = df_filtered.groupby(["classe", "annee"], as_index=False)["boites"].sum()
    df_overview["annee"] = df_overview["annee"].astype(str)
    class_bar_chart(df_overview)

    st.write("The antidepressants category significantly increased between 2019 and 2025. The Z-drugs category has also decreased. The lithium seems to have increased (hard to tell how much), anxiolytics and hypnotics have decreased.")
    st.write("Let's estimate those changes numerically...")

    # ---- 2 - Precise evolution ----------------------------------------------------
    st.header("2 - What really changed ?")
    st.caption("Evolution by percentage relative to baseline year. Each class is compared with itself since treatment durations vary across classes.")

    by_class = df_filtered.groupby(["annee", "classe"])["boites"].sum().unstack()
    if not by_class.empty and len(by_class) > 1:
        df_pct = ((by_class / by_class.iloc[0] - 1) * 100).reset_index()
        df_melted = df_pct.melt(id_vars=["annee"], var_name="classe", value_name="pct_change")
        years = [int(y) for y in by_class.index]
        st.altair_chart(pct_change_line(df_melted, years, years[0]), width="stretch")

    st.text("Between 2016 and 2025 antidepressants are up about 40%, and about 90% of that rise comes after 2019 (+5% by 2019). Lithium (+40%) and antipsychotics (+15%) also grew.")
    st.text("During the first year of the pandemic, EPI-PHARE already observed about 1.9 million more antidepressant dispensations than expected (March 2020 – April 2021). During the same period, they were also an increase of 3.4 million anxiolytics and 1.4 million hypnotics [3].")
    st.text("These increases could have been influenced the 2020-2021 isolation [4]")
    st.text("For Z-drugs, the fall predates COVID. Zolpidem has required a secure prescription since April 2017, after addictovigilance surveys showed rising abuse and dependence [5]. This is one plausible explanation for the Z-drug decline.")

    reference(3)
    reference(4)
    reference(5)
