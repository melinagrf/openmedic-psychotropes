"""Bibliography: one place for every reference cited in the app ([1] … [8])."""

import streamlit as st

# number -> (expander title, url, full citation or None)
REFERENCES = {
    1: (
        "[1] World Health Organization Report 2022",
        "https://www.who.int/publications/i/item/9789240051157",
        "Source: World Health Organization. (2022). World health statistics 2022: Monitoring health for the SDGs. World Health Organization.",
    ),
    2: (
        "[2] Santé publique France Rapport 2021",
        "https://documentation.insp.gouv.fr/insp/doc/VIEPUBLIQUE/220D47BB9B1A06179E586C6B732E3725/sante-publique-france-rapport-annuel-2021?_lg=fr-FR",
        None,
    ),
    3: (
        "[3] ANSM / EPI-PHARE, 6th report on drug use during COVID-19 (May 2021)",
        "https://www.epi-phare.fr/rapports-detudes-et-publications/covid-19-usage-des-medicaments-rapport-6/",
        "Source:Weill, A., Drouin, J., Desplas, D., Cuenot, F., Dray-Spira, R., & Zureik, M. (2021). Usage des médicaments de ville en France durant l’épidémie de la Covid-19 – point de situation jusqu’au 25 avril 2021. Étude pharmaco-épidémiologique à partir des données de remboursement du SNDS.",
    ),
    4: (
        "[4] Link between depression [and anxiety] during the COVID",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC9685018/",
        "Source: Zhu C, Zhang T, Li Q, Chen X, Wang K. Depression and Anxiety During the COVID-19 Pandemic: Epidemiology, Mechanism, and Treatment. Neurosci Bull. 2023 Apr",
    ),
    5: (
        "[5] French national addictovigilance follow-up of zolpidem between 2014 and 2020: evolution of drug abuse, misuse and dependence before and after the regulatory change",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC10066475/",
        "Aquizerate A, Laforgue EJ, Istvan M, Rousselet M, Gerardin M, Jouanjus E, Libert F; French Addictovigilance Network; Guerlais M, Victorri-Vigneau C. French national addictovigilance follow-up of zolpidem between 2014 and 2020: evolution of drug abuse, misuse and dependence before and after the regulatory change. Eur J Public Health. 2023 Apr 1",
    ),
    6: (
        "[6] Antipsychotic off-label use in the 21st century: An enduring public health concern",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11789223/",
        "Source: Verdoux H. Antipsychotic off-label use in the 21st century: An enduring public health concern. Dialogues Clin Neurosci. 2025 Dec",
    ),
    7: (
        "[7] Is the diagnosis and treatment of depression gender-biased? Evidence from a population-based aging cohort in Sweden",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11600552/",
        "Source: Bacigalupe A, Martín U, Triolo F, Sjöberg L, Sterner TR, Dekhtyar S, Fratiglioni L, Calderón-Larrañaga A. Is the diagnosis and treatment of depression gender-biased? Evidence from a population-based aging cohort in Sweden. Int J Equity Health. 2024 Nov 27",
    ),
    8: (
        "[8] Santé Mentale – HCFEA report on psychotropics in children (March 2023)",
        "https://www.santementale.fr/2023/03/surconsommation-psychotropes-chez-enfant-et-adolescent-rapport-sonne-alarme/",
        None,
    ),
}


def reference(number: int) -> None:
    """Render reference [number] as a collapsed expander."""
    title, url, citation = REFERENCES[number]
    with st.expander(title):
        st.write(url)
        if citation:
            st.write(citation)
