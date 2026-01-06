# Streamlit Dashboard Project: SEA-AD Donor & Pathology Explorer

**Author:** Lucie Benoit | [lucie.benoit@efrei.fr](mailto:lucie.benoit@efrei.fr)
**Project Type:** Individual Project

---

## Project Overview

This interactive **Streamlit dashboard** explores the **SEA-AD dataset**, providing insights into **Alzheimer’s disease pathology across donors**.

It allows users to visualize **demographics, genetic risk factors (APOE4), neuropathological burden (ADNC), and cellular markers (pTau, Aβ, NeuN, GFAP, IBA1)**, helping researchers understand **how Alzheimer’s disease progresses across individuals and at the tissue/cellular level**.

The dashboard is designed to **support exploration of the SEA-AD atlas**, facilitating a better understanding of the relationship between pathology, genetics, and clinical status.

---

## Deployed App

Access the live dashboard here: [Deployed App URL](#)

---

## Repository

Source code and project files: [GitHub Repository](#)

---

## Demo Video

Watch a walkthrough of the app: [Demo Video Link](#)

---

## Dataset

* Dataset name: **SEA-AD cohort datasets**
* Source: [Allen Institute SEA-AD Project](https://www.nature.com/articles/s41593-024-01774-5)
* License: Please follow the [Allen Institute Terms of Use](https://alleninstitute.org/legal/terms-of-use/)

The dashboard uses curated SEA-AD data, including:

* **Donor metadata:** demographics, clinical status, APOE genotype, dementia status
* **Quantitative neuropathology:** Aβ, pTau (AT8), GFAP, IBA1, NeuN
* **Harmonized clinical measures:** dementia/clinical cognitive status

Coverage: **Multiple donors across the full spectrum of Alzheimer’s disease pathology.**

Additional references consulted for context and biological background:
- Nature Neuroscience paper: [Integrated multimodal cell atlas of Alzheimer’s disease](https://www.nature.com/articles/s41593-024-01774-5)
- NIH resource: [Alzheimer’s Disease Genetics Fact Sheet](https://www.nia.nih.gov/health/alzheimers-causes-and-risk-factors/alzheimers-disease-genetics-fact-sheet)
---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/lucie-benoit/streamlit-sea-ad.git
```

2. Navigate to the project folder:

```bash
cd streamlit-sea-ad
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

---

## Usage

Use the sidebar controls to select **Dashboard Overview or Brain pathology (MTG)**.

Navigate through sections using the radio button panel:

* **Cohort Overview:** Demographics, genetic risk (APOE4), and clinical status across donors
* **Brain Pathology (MTG):** pTau, Aβ, NeuN distributions, correlations, and neuronal integrity analyses


---

## Features

* **Interactive Visualizations:** Histograms, donut charts, scatter plots, and heatmaps for key pathology markers
* **Donor-Level Analysis:** Explore age, sex, APOE genotype, dementia status, and ADNC across donors
* **Neuropathology Insights:** Quantitative measures of tau, amyloid, and neuronal/glial markers
* **Correlation Analyses:** Relationships between pathologies and neuronal integrity
* **Continuum of Disease Severity:** Track how pathology progresses across ADNC stages

---

## Notes

* Cognitive scores are **not included**; the app focuses on **clinical status and neuropathology**
* All visualizations are based on **quantitative measurements from MTG**
* Users should **cite the SEA-AD dataset and primary publication** when using these data


