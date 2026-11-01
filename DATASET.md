# Dataset used

**Open Medic — base complète sur les dépenses de médicaments interrégimes**
Producer: CNAM (Assurance Maladie), extracted from the SNDS/Sniiram national claims system.

| Item | Value |
|---|---|
| Portal | data.gouv.fr (approved portal) |
| Dataset page | https://www.data.gouv.fr/datasets/open-medic-base-complete-sur-les-depenses-de-medicaments-interregimes |
| Producer page | https://assurance-maladie.ameli.fr/etudes-et-donnees/open-medic-base-complete-depenses-medicaments |
| Variable descriptions | https://www.assurance-maladie.ameli.fr/content/descriptif-des-variables-de-la-serie-open-medic |
| Yearly files used | 2016, 2019, 2025 |
| Licence | Open Licence (Etalab) — reuse allowed with attribution |
| Content | Reimbursed medicines dispensed in city pharmacies: boxes, reimbursed amounts, by ATC class, patient age group, sex and region |

## Prepared table used by the app

The three yearly files were filtered on psychotropic drugs (ATC codes), grouped into six classes
(antidepressants, antipsychotics, anxiolytics (benzodiazepines), hypnotics (benzodiazepines),
Z-drugs, lithium), merged, and reduced to the columns below. The result is
`data/openmedic_psychotropes.csv`.

| Column | Meaning |
|---|---|
| `annee` | Year (2016, 2019, 2025) |
| `classe` | Psychotropic class (French label in the CSV, translated to English by the app) |
| `atc`, `atc_label` | ATC code and molecule name |
| `age` | Age group: 0-19, 20-59, 60 and over |
| `sexe` | Females / Males |
| `region_code`, `region` | Patient region (code and name) |
| `boites` | Number of boxes dispensed |
| `rem` | Amount reimbursed (€) |
| `bse` | Reimbursement base (€) |

Other sources (reports and articles cited as [1]–[8]) are listed in the app itself, in the
collapsible reference boxes.
