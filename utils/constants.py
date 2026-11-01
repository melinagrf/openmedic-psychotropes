"""Constants shared across the app (palettes, label sets, regional reference data).

The app does no random sampling and uses no random numbers: every run on the same
CSV gives exactly the same output, so no seed is needed.
"""

PASTEL_PALETTE = [
    "#A27CA2",  # Violet
    "#8DA9C4",  # Bleu
    "#94D2BD",  # Sauge
    "#F4A261",  # Pêche
    "#E7C6FF",  # Rose
]

# Colours of the three molecule bar charts (section 3) and of the gender split (section 4)
COLOR_ANTIDEPRESSANTS = "#A27CA2"
COLOR_ANTIPSYCHOTICS = "#8DA9C4"
COLOR_BENZODIAZEPINES = "#94D2BD"
GENDER_COLORS = ["#8DA9C4", "#A27CA2"]  # Females, Males

# --- Translation of the French labels of the prepared CSV --------------------------
CLASS_TRANSLATION = {
    "Antidepresseurs": "Antidepressants",
    "Antipsychotiques": "Antipsychotics",
    "Anxiolytiques (benzodiazepines)": "Anxiolytics (benzodiazepines)",
    "Anxiolytiques(benzodiazepines)": "Anxiolytics (benzodiazepines)",
    "Hypnotiques (Z-drugs)": "Z-drugs",
    "Hypnotiques (benzodiazepines)": "Hypnotics (benzodiazepines)",
    "Lithium": "Lithium",
}
GENDER_TRANSLATION = {"Femmes": "Females", "Hommes": "Males"}
AGE_TRANSLATION = {
    "0-19 ans": "0-19 yo",
    "20-59 ans": "20-59 yo",
    "60 ans et +": "60 yo and older",
}

UNKNOWN = "Inconnu"  # label used in the CSV for unmapped regions / ages / genders

# --- Drug-class groups used in section 3 --------------------------------------------
ANTIDEPRESSANT_CLASSES = ["Antidepresseurs", "Antidepressants"]
ANTIPSYCHOTIC_CLASSES = ["Antipsychotiques", "Antipsychotics"]
BENZODIAZEPINE_CLASSES = [
    "Anxiolytiques(benzodiazepines)",
    "Hypnotiques (benzodiazepines)",
    "Anxiolytics (benzodiazepines)",
    "Hypnotics (benzodiazepines)",
]

# --- Regional reference data (INSEE) ------------------------------------------------
# Approximate geographic centres (lat, lon) used to place the markers of the maps
CENTRES = {
    "11": (48.71, 2.50), "24": (47.55, 1.70), "27": (47.18, 4.80), "28": (49.18, 0.40),
    "32": (50.00, 2.80), "44": (48.70, 5.60), "52": (47.50, -0.80), "53": (48.20, -2.90),
    "75": (45.30, 0.30), "76": (43.70, 2.20), "84": (45.40, 4.90), "93": (43.95, 6.05),
    "94": (42.15, 9.10),
}

# Region code -> official name (the CSV has unaccented names, so codes are the reliable key)
REGION_NAMES = {
    "11": "Île-de-France", "24": "Centre-Val de Loire", "27": "Bourgogne-Franche-Comté",
    "28": "Normandie", "32": "Hauts-de-France", "44": "Grand Est",
    "52": "Pays de la Loire", "53": "Bretagne", "75": "Nouvelle-Aquitaine",
    "76": "Occitanie", "84": "Auvergne-Rhône-Alpes", "93": "Provence-Alpes-Côte d'Azur",
    "94": "Corse",
}

# In the CSV, region code 5 is labelled "Code a verifier : 5" (overseas territories, unusable)
OVERSEAS_CODE = "05"
OVERSEAS_LABEL = "DOM-TOM (code 5, to verify)"

# Rounded INSEE population by region code (one value used for all years)
POPULATION_BY_CODE = {
    "11": 12200000, "84": 8100000, "75": 6000000, "76": 6000000, "32": 6000000,
    "44": 5500000, "93": 5100000, "52": 3800000, "53": 3300000, "28": 3300000,
    "24": 2500000, "27": 2800000, "94": 350000,
}
