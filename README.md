# How are the French doing? Psychotropic drugs in France (2016–2025)

Interactive Streamlit data-storytelling app on psychotropic drug dispensing in France, built from the Open Medic open data (Assurance Maladie), for 2016, 2019 and 2025.

## Questions
- How are mental-health challenges reflected in pharmacy dispensing data?
- How did prescription patterns change since 2016, including the 2019–2020 crisis?
- Who is the most affected among the French population?

## Data
- **Open Medic** (Assurance Maladie), 2016, 2019 and 2025, from [data.gouv.fr](https://www.data.gouv.fr/) (Licence Ouverte).
- Only psychotropic drugs (ATC codes) were kept and grouped into classes: antidepressants, antipsychotics, benzodiazepines, Z-drugs and lithium.
- Dimensions kept: year, drug class and molecule, age band, sex, region, boxes dispensed and reimbursement.
- Region outlines: [france-geojson](https://github.com/gregoiredavid/france-geojson).

## Main limit
The data counts **boxes dispensed, not patients**. A rise can come from longer treatments, regulation or reimbursement rules, not only from more people treated.

## Run it
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
- `app.py`: the Streamlit app
- `scripts/`: data preparation (`merge_openmedic.py`) and exploration (`explore.py`)
- `data/`: processed table and region outlines

## Stack
Python, pandas, Streamlit, Plotly
