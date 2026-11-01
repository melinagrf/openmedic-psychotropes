# openmedic-psychotropes
Interactive Streamlit data-storytelling app on psychotropic drug dispensing in France (Open Medic, 2016–2019–2025): trends by class, molecules, age/sex and region.

# How are the French doing ? — psychotropic drug dispensing in France

Individual project — Data Storytelling Dashboard with Streamlit (StApp26, #EFREIDataStories2026)
Author: Melina GARUFI — EFREI Paris, ING2 DAI, 2026-2027

- Deployed app: `<URL of the deployed app>`
- Demo video (2–4 min): `<link to the video>`
- Storyboard: `<link to the storyboard>`

## Story

**Hook.** Mental health became a major public-health issue over the past decade (COVID-19, rising depressive episodes).
**Questions.** How is this reflected in pharmacy dispensing data? How did prescriptions change since 2016? Who is the most affected?
**Narrative.** Overview by drug class → relative change → which molecules drive it → who (age, gender) → where (regions) → insights, limits, ethics.
**Audience.** Students and the general public interested in public-health data.

## Data

Open Medic (CNAM / data.gouv.fr, Open Licence), yearly files 2016, 2019 and 2025, restricted to
psychotropic drugs. Full links, licence and column dictionary: see [`DATASET.md`](DATASET.md).

The app reads one prepared table (14,324 rows, included in the zip) located at:

```
data/openmedic_psychotropes.csv
```

If the file is missing, the app shows an explicit message instead of crashing. Region names are rebuilt from the region codes (the CSV has unaccented names) and region code 5 (overseas territories) is flagged and left out of the regional rankings.
Raw yearly Open Medic files are not bundled (they are large): download them from the links in
`DATASET.md`; the preparation steps (psychotropic ATC filter, class grouping, merge of the three
years, column selection) are described there.

## Run locally

Python 3.11 or newer (tested with 3.13).

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```

`make install` and `make run` do the same on macOS/Linux. Dependencies are pinned in
`requirements.txt`; the app uses no random sampling, so results are identical on every run.

## Project structure

```
app.py                 entry point: page config, data loading, order of the story
sections/
  intro.py             hook, context, questions, dataset presentation, definitions
  quality.py           data-quality audit (values computed from the data)
  sidebar.py           filters: region, year, drug class
  overview.py          KPIs, section 1 (classes), section 2 (relative change)
  deep_dives.py        section 3 (molecules), 4 (age/gender), 5 (regions/maps), 6 (heatmap)
  conclusions.py       key insights, limitations, ethics
utils/
  io.py                load_data() with st.cache_data, paths, licence text
  prep.py              quality audit, filters, KPIs, molecule and regional aggregations
  viz.py               chart functions (consistent style)
  refs.py              bibliography [1]–[8]
  constants.py         palettes, label translations, regional reference data (INSEE)
data/                  openmedic_psychotropes.csv goes here
assets/                images (optional)
```

## Features (as required)

- Sidebar filters (region, year, drug class) that drive the KPIs and the charts.
- KPI header tied to the filters: boxes, reimbursement, average cost per box for the latest selected year vs the reference year.
- Interactive visuals with tooltips: grouped bars, evolution lines, molecule bars with sliders, age/gender panels, maps (top 5 regions), heatmap.
- Data-quality section: duplicates, missing values, unmapped regions/ages/genders, negative values, types.
- Performance: `st.cache_data` on data loading and on the quality audit; aggregations done on the prepared table.

## Limitations

- A box is not a patient: longer treatments can raise the number of boxes without more people treated.
- Only three years (2016, 2019, 2025): the pandemic effect cannot be separated from long-term trends.
- Regional rates use one rounded INSEE population per region for all years and are not age-standardised.
- Overseas territories are not usable in the dataset (see the app, section 5).
- The dataset gives the drug class, not the reason for prescription.
- The app is descriptive and does not establish causality.
