"""Key insights, limitations, ethics."""

import streamlit as st


def render_conclusions() -> None:
    st.markdown("### Key insights")
    st.write("The pandemic may have increased mostly antidepressants dispensing, but also some hypnotics and anxiolytics dispensing.")
    st.write("The dispensing of Z-drugs has significantly decreased (-39%), it is likely due to the risks of abuse and dependence.")
    st.write("Antipsychotics are more and more prescribed. Some studies link this increase to off-labels prescriptions.")
    st.write("Women are more likely to be prescribed antidepressants, scientist are investigating whether it is a gender bias.")

    st.markdown("### Data Quality & Limitations")
    st.write(" Reimbursement figures exclusively cover outpatient pharmacy prescriptions reimbursed by the french healthcare system. Non-reimbursed drugs and inpatient hospital administration are excluded from Open Medic records.")
    st.write("Boxes are not patients : a box can cover one month or several, so a rise may come from longer treatments rather than more people treated")
    st.write("Pandemic effects cannot be separated from longer trends with only three years.")
    st.write("Only metropolitan France can be analysed: DOM-TOM rows are grouped under a single region code (5) and are left out of the regional analysis.")
    st.write("The dataset gives a drug class but not the exact reason the psychotropic has been prescribed for (eg some antidepressants (TCAs) are used for pain management).")

    st.markdown("### Ethics")
    st.write("This dashboard serves purely as a descriptive tool for monitoring prescription patterns; it does not draw direct causal conclusions without controlling for local healthcare supply and socio-economic factors.")

    st.divider()
    st.write("Melina GARUFI ING2 DAI 2026-2027")
