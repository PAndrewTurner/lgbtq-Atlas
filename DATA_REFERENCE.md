# LGBTQ+ Atlas — Developer Data Reference

> **Purpose:** Complete reference for all datasets collected for the LGBTQ+ Atlas web app. Covers file paths, schemas, column definitions, geographic granularity, join keys, use cases, and known data caveats. Intended to be passed as context to Claude Code during web app development.
>
> **Data root:** `data/raw/` (relative to project root)  
> **Last updated:** 2026-04-27  
> **Total files:** 105 | **~187MB on disk**

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Geographic Coverage Matrix](#2-geographic-coverage-matrix)
3. [Population & Demographics](#3-population--demographics)
4. [Legal & Policy Climate](#4-legal--policy-climate)
5. [Safety Data](#5-safety-data)
6. [Health & Wellbeing](#6-health--wellbeing)
7. [Economic Data](#7-economic-data)
8. [Community Infrastructure](#8-community-infrastructure)
9. [Youth Data](#9-youth-data)
10. [Socioeconomic & Household Profiles](#10-socioeconomic--household-profiles)
11. [Geographic Reference Files](#11-geographic-reference-files)
12. [Join Keys & Data Relationships](#12-join-keys--data-relationships)
13. [Files Requiring Manual Extraction](#13-files-requiring-manual-extraction)
14. [Known Data Gaps](#14-known-data-gaps)
15. [Critical Display Caveats](#15-critical-display-caveats)

---

## 1. Architecture Overview

All downloaded data lives under `data/raw/` in category subdirectories:

```
data/raw/
├── population/         # Census ACS household/couple tables, Williams Institute estimates
├── legal/              # HRC MEI/SEI/HEI/CEI indices, Trans Legislation Tracker, FBI hate crime
├── safety/             # FBI hate crime CSV (same file symlinked from legal/)
├── health/             # Trevor Project, GLSEN, Williams Institute health PDFs
├── economic/           # Williams Institute economic PDFs, BLS OEWS instructions
├── community/          # IRS/NCCS nonprofit registry
├── youth/              # CDC YRBSS SOGI data
├── socioeconomic/      # Census ACS socioeconomic tables, Gallup, Williams Institute PDFs
└── geo/                # TIGER/Line shapefiles, FIPS code tables
```

### Data Formats Summary

| Format | Count | Notes |
|--------|-------|-------|
| CSV (ready for pipeline) | 21 | Machine-readable, column names in plain English |
| PDF (needs extraction) | ~75 | Williams Institute, Trevor Project, HRC, GLSEN |
| Shapefile ZIP | 4 | TIGER/Line boundary files |
| TXT | 3 | FIPS crosswalks, download instructions |

### Key Design Principle

**CSVs are ready to use. PDFs require table extraction before they can power the app.** The most important PDFs to extract are the Trevor Project 50-state reports and the HRC SEI scorecard — these are the richest state-level qualitative data we have. See [Section 13](#13-files-requiring-manual-extraction).

---

## 2. Geographic Coverage Matrix

Which data exists at which geographic level:

| Dataset | National | State | County | City/Metro |
|---------|:--------:|:-----:|:------:|:----------:|
| Census B11009 (same-sex couples) | — | ✅ 52 | ✅ 3,222 | — |
| Williams Institute pop. estimates | ✅ | ✅ 51 | — | — |
| Gallup LGBTQ+ identification | ✅ | ⚠️ sub only | — | — |
| HRC MEI city scores | — | — | — | ✅ 506 cities |
| HRC SEI state ratings | — | ✅ 50 | — | — |
| HRC HEI facility ratings | — | — | — | ✅ 1,065+ facilities (PDF) |
| FBI hate crimes (LGBTQ+ biases) | ✅ | ✅ 51+DC | — | — |
| Trans legislation tracker | ✅ | ✅ 49 | — | — |
| Trevor Project mental health | ✅ | ✅ 50 | — | — |
| GLSEN school climate | ✅ | — | — | — |
| CDC YRBSS SOGI | ✅ | ✅ partial | — | ✅ urban districts |
| IRS LGBTQ+ nonprofits | — | ✅ | ✅ via zip | ✅ city-level |
| Census socioeconomic (B11001, etc.) | — | ✅ 52 | ✅ 3,222 | — |
| TIGER/Line boundaries | — | ✅ | ✅ | ✅ CBSA |

**Bottom line for map layers:**
- **National overview:** Gallup trends, Williams Institute estimates
- **State choropleth:** HRC SEI rating, FBI hate crime rates, trans legislation count, Trevor Project metrics (after PDF extraction), Census same-sex household density
- **County choropleth:** Same-sex household count/rate, socioeconomic indicators
- **City/point layer:** HRC MEI scores (506 cities), LGBTQ+ nonprofits (~5,000 org points)

---

## 3. Population & Demographics

### 3.1 Census ACS B11009 — Same-Sex Couples

The most important Census dataset for this app. Directly counts same-sex married and cohabiting couples by household type.

**Files:**
- `population/census_acs_B11009_state_2024.csv` — 52 rows (all states + DC)
- `population/census_acs_B11009_state_2024_1yr.csv` — 52 rows (1-year ACS, higher MoE)
- `population/census_acs_B11009_county_2024.csv` — 3,222 rows

**Schema (all three files):**

| Column | Type | Definition |
|--------|------|------------|
| `geography` | string | Full state/county name |
| `total_households` | int | Total occupied housing units |
| `married_couple_households` | int | All married couple households |
| `opposite_sex_married_households` | int | Married opposite-sex couples |
| `same_sex_married_households` | int | Married same-sex couples (sum of next two) |
| `male_male_married_households` | int | Married male-male couples |
| `female_female_married_households` | int | Married female-female couples |
| `cohabiting_couple_households` | int | All unmarried partner households |
| `opposite_sex_cohabiting_households` | int | Cohabiting opposite-sex |
| `same_sex_cohabiting_households` | int | Cohabiting same-sex (sum of next two) |
| `male_male_cohabiting_households` | int | Cohabiting male-male |
| `female_female_cohabiting_households` | int | Cohabiting female-female |
| `all_other_households` | int | Non-couple family + single-person households |
| `state_fips` | string (2-char) | State FIPS code |
| `county_fips` | string (3-char) | County FIPS (county file only) |

**Derived fields to compute:**
- `total_same_sex_households` = `same_sex_married_households` + `same_sex_cohabiting_households`
- `same_sex_share_of_all_couples` = `total_same_sex_households` / (`married_couple_households` + `cohabiting_couple_households`)
- Join key to shapefiles: `state_fips` (2-char) or `state_fips + county_fips` (5-char FIPS)

**Caveats:**
- ACS 5-year estimates; margins of error exist (not included in download, re-query with `MOE` variables if needed)
- In small counties, same-sex household counts may be suppressed (appear as empty/0)
- Prefer 5-year over 1-year for state comparisons; 1-year is only reliable for large-population states
- These are *couple households*, not LGBTQ+ population — individuals without partners are not counted

---

### 3.2 Williams Institute Population Estimates

**File:** `population/williams_population_estimates_2023.pdf` (PDF — needs extraction)

**What's inside:** State-by-state estimates of the total LGBT adult population (count and % of adults), broken down by:
- Gender identity (LGB vs. transgender)
- Race/ethnicity (White, Black, Hispanic, Asian, Other)
- Age groups (18–24, 25–34, 35–49, 50–64, 65+)
- Urban/rural classification

**Key national figure:** ~7.6% of U.S. adults identify as LGBT (2023). State range: ~5% (more rural states) to ~10%+ (CA, OR, VT, MA, NV).

**Extraction target:** `population/williams_population_estimates_extracted_2023.csv`
Suggested schema: `state`, `state_abbr`, `lgbtq_adult_count`, `lgbtq_pct_of_adults`, `transgender_count`, `transgender_pct`, `source`, `vintage`

---

### 3.3 Gallup LGBTQ+ Identification

**Files:**
- `socioeconomic/gallup_lgbtq_demographics_2024.csv` — National breakdowns by generation and identity type
- `socioeconomic/gallup_lgbtq_national_trend_2012_2024.csv` — 12-year national trend

**Schema (demographics file):**

| Column | Definition |
|--------|------------|
| `category` | Breakdown dimension (generation, identity_type, overall) |
| `group` | Group label (e.g., "Gen Z", "Bisexual", "Overall") |
| `lgbtq_pct` | Percent identifying as LGBTQ+ |
| `year` | Survey year (2024) |
| `source` | "Gallup" |

**Key figures:**
- Overall: 9.3% of U.S. adults (2024)
- Gen Z (born 1997–2012): 22.3%
- Millennials (1981–1996): 11.5%
- Gen X (1965–1980): 5.6%
- Boomers (1946–1964): 2.5%
- Bisexual: 4.5% | Gay/Lesbian: 2.2% | Transgender: 1.1%

**Trend file schema:** `year`, `lgbtq_pct`, `source`
Covers 2012 (3.5%) → 2024 (9.3%) — good for a trend line chart.

**Caveat:** State-level Gallup data requires a paid subscription. National data only in these files.

---

## 4. Legal & Policy Climate

### 4.1 HRC Municipal Equality Index — City Scores

**File:** `legal/hrc_mei_city_scores_2025.csv` ✅ Ready to use

**Schema:**

| Column | Type | Definition |
|--------|------|------------|
| `city` | string | Municipality name |
| `state` | string (2-char) | State abbreviation |
| `mei_score` | int (0–100) | Overall MEI composite score |
| `hrc_slug` | string | URL path segment for HRC detail page (e.g., `new-york-city-ny`) |

**Coverage:** 506 cities across all 50 states. 132 cities score 100 (perfect). Mean = 70.1. Min = 0.

**Use cases:**
- City-level point layer on map, colored by score
- Filter to show only cities above/below a threshold
- Link to HRC detail page: `https://www.hrc.org/resources/municipalities/{hrc_slug}`
- Rank cities by state for a "best/worst cities in your state" view

**The 5 MEI scoring categories** (from HRC documentation; subcategory scores require individual city pages):
1. Non-Discrimination Laws (private employment, housing, public accommodations, city employment, trans healthcare benefits)
2. Municipality as Employer (city employment protections, trans healthcare in city benefits)
3. Municipal Services (LGBTQ+ liaison, human rights commission)
4. Law Enforcement (LGBTQ+ police liaison/task force, hate crime reporting to FBI)
5. Leadership on LGBTQ+ Equality (openly LGBTQ+ elected/appointed leaders)

**Geocoding needed:** This file has city + state but no lat/lon. You'll need to geocode for map placement. Use the Census Geocoding API or a lookup table. Many of the 506 cities are large enough to find in Census place data.

---

### 4.2 HRC Municipal Equality Index — Full Report PDFs

- `legal/hrc_mei_2025.pdf` (313KB) — 2025 narrative report
- `legal/hrc_mei_2024.pdf` (320KB) — 2024 report (for year-over-year)

These are 36-page narrative reports. The city score CSV above supersedes them for data purposes. Use PDFs for context, methodology descriptions, and UI copy.

---

### 4.3 HRC State Equality Index

**File:** `legal/hrc_sei_2024_national_scorecard.pdf` (347KB) — Needs extraction

**What's inside:** All 50 states rated across four categories:
1. **Relationship & Parental Recognition** — marriage, adoption, 2nd-parent adoption, foster care
2. **Non-Discrimination Protections** — employment, housing, public accommodations, credit, education
3. **Religious Exemptions** — broad religious freedom laws that allow discrimination
4. **Healthcare & Safety Laws** — LGBTQ+ healthcare bans, conversion therapy bans, hate crime laws

**Rating scale per category:** High / Medium / Low / Negative  
**Overall state climate:** Solidly Inclusive → Working Toward Inclusion → Stagnating → Attempting to Legislate Exclusion → Actively Hostile

**Extraction target:** `legal/hrc_sei_2024_extracted.csv`
Suggested schema: `state`, `state_abbr`, `relationship_recognition_rating`, `nondiscrimination_rating`, `religious_exemption_rating`, `healthcare_safety_rating`, `overall_climate`, `year`

**Use case:** State choropleth showing legal climate. Great for a "legal climate score" layer. Pair with FBI hate crime data for a combined "climate + safety" view.

---

### 4.4 HRC Healthcare Equality Index

**File:** `legal/hrc_hei_2024_executive_summary.pdf` (5.0MB)

**What's inside:** 1,065+ healthcare facilities rated 0–100 on LGBTQ+ patient care policies. Categories: non-discrimination in patient care, visitor policies, employment protections, staff training, transgender-inclusive care.

**Use case:** "Find LGBTQ+-affirming healthcare near me" map layer. Full facility-level data (with addresses) available at `https://www.hrc.org/resources/healthcare-equality-index` — requires scraping or HRC data request. This PDF provides national/summary context only.

---

### 4.5 HRC Corporate Equality Index

- `legal/hrc_cei_2025_corporate_citizens.pdf` (6.6MB) — 1,300+ employers rated
- `legal/hrc_cei_2025_appendix_a_companies.pdf` (1.1MB) — Full company list with scores

**Use case:** "LGBTQ+-friendly employers" layer. Cross-reference employer HQ city with MEI scores. Appendix A has extractable company name + score table — target: `legal/hrc_cei_2025_companies_extracted.csv`.

---

### 4.6 Trans Legislation Tracker

**Files:**
- `legal/trans_legislation_tracker_2025_state.csv` — Bills by state, 2025 session
- `legal/trans_legislation_tracker_2025_categories.csv` — Bills by category nationally
- `legal/trans_legislation_tracker_national_trend.csv` — 2023–2025 annual totals

**Schema (state file):**

| Column | Definition |
|--------|------------|
| `state` | State name |
| `bills_introduced_2025` | Count of anti-trans bills introduced in 2025 session |
| `year` | 2025 |
| `source` | "Trans Legislation Tracker" |

**Key stats:**
- 2025: 1,022 bills introduced; 126 passed
- 2024: 701 bills; 51 passed
- 2023: 615 bills; 87 passed

**Categories (top 5):** Education (280), Healthcare (214), Other (174), Sports (127), Public facilities (80)

**Use case:** State choropleth of legislative hostility. Pair with HRC SEI for comprehensive policy climate layer.

---

### 4.7 FBI Hate Crimes (LGBTQ+ Bias Categories)

**File:** `legal/fbi_hatecrimes_lgbtq_2019_2024.csv` (also in `safety/`) ✅ Ready to use

**Schema:**

| Column | Type | Definition |
|--------|------|------------|
| `geography` | string | State abbreviation or "national" |
| `state_abbr` | string | 2-char state code; "US" for national |
| `year` | int | 2019–2024 |
| `anti_gay_male` | int | Incidents with Anti-Gay (Male) bias motivation |
| `anti_lesbian_female` | int | Anti-Lesbian (Female) incidents |
| `anti_lgbtq_mixed` | int | Anti-Lesbian, Gay, Bisexual, or Transgender (Mixed Group) |
| `anti_transgender` | int | Anti-Transgender incidents |
| `anti_gender_nonconforming` | int | Anti-Gender Non-Conforming incidents |
| `anti_bisexual` | int | Anti-Bisexual incidents |
| `total_lgbtq_incidents` | int | Sum of all 6 LGBTQ+ bias categories |
| `total_sexual_orientation` | int | Gay male + Lesbian + Mixed + Bisexual |
| `total_gender_identity` | int | Transgender + Gender Non-Conforming |
| `total_all_hate_crimes` | int | All hate crime incidents reported by that geography/year |

**Coverage:** 312 rows = (national + 50 states + DC) × 6 years (2019–2024)

**National LGBTQ+ trend:**
```
2019: 1,537 → 2020: 1,702 → 2021: 2,272 → 2022: 2,689 → 2023: 2,899 → 2024: 2,658
```

**Top states 2024:** CA (573), NJ (213), WA (144), NY (134)

**Derived fields to compute:**
- `lgbtq_share_of_all_hate_crimes` = `total_lgbtq_incidents` / `total_all_hate_crimes`
- `lgbtq_rate_per_100k` = `total_lgbtq_incidents` / state_population × 100,000 (needs population join)
- Year-over-year change: compare same geography across years

**Critical caveats for UI display:**
1. Raw counts must NOT be compared across states without normalization. CA has more incidents partly because it has more agencies reporting.
2. Many jurisdictions don't report hate crimes at all — these numbers are a **floor**, not a ceiling.
3. The NIBRS transition (2021–2023) affects year-over-year comparability. Some states' counts changed because of reporting system changes, not actual crime changes.
4. Always show a disclaimer on any hate crime visualization.

**API source for updates:** `https://cde.ucr.cjis.gov/LATEST/hate-crime/state/{STATE}/?from=01-{YEAR}&to=12-{YEAR}&type=totals`

---

## 5. Safety Data

Primary safety dataset is the FBI hate crime CSV documented in Section 4.7.

**Additional safety context** (not yet in CSV form):
- NCAVP/AVP annual LGBTQ+ hate violence reports — `https://avp.org/ncavp/` — these cover reported incidents to LGBTQ+ anti-violence programs (different from FBI UCR; often higher counts due to direct community reporting)

---

## 6. Health & Wellbeing

### 6.1 Trevor Project — 2024 State Mental Health Survey

This is the richest state-level LGBTQ+ youth data in the dataset. All 50 state PDFs are downloaded.

**Files:**
- `health/trevorproject_survey_2024.pdf` — National report (7.4MB)
- `health/trevorproject_survey_2024_{StateName}.pdf` — One per state, ~1.8MB each
  - Single-word states: `trevorproject_survey_2024_California.pdf`
  - Multi-word states use CamelCase: `trevorproject_survey_2024_NewYork.pdf`, `trevorproject_survey_2024_NorthCarolina.pdf`

**Key metrics available per state (in PDF tables):**
- % LGBTQ+ youth who seriously considered suicide in the past year
- % who attempted suicide in the past year
- % who wanted but could not access mental health care
- % exposed to conversion therapy
- % who felt safe at school
- % with at least one accepting adult in their life
- % whose home was not LGBTQ+-affirming

**Extraction target:** `health/trevorproject_survey_2024_extracted.csv`
Suggested schema: `state`, `state_abbr`, `pct_considered_suicide`, `pct_attempted_suicide`, `pct_no_mental_health_access`, `pct_conversion_therapy_exposed`, `pct_felt_safe_school`, `pct_accepting_adult`, `year`

**Coverage:** 18,000+ LGBTQ+ youth aged 13–24. Survey conducted 2023–2024.

**Use case:** State choropleth for youth mental health crisis severity. Most compelling data for advocacy context in the app.

---

### 6.2 GLSEN National School Climate Survey

**File:** `health/glsen_nscs_2024_toolkit.pdf` (1.7MB) — National only

**Key metrics (national):**
- % of LGBTQ+ students who felt unsafe at school because of sexual orientation
- % who heard homophobic remarks from teachers/staff
- % in schools with GSAs
- % in schools with inclusive anti-bullying policies
- % in schools with LGBTQ+-inclusive curriculum

**Caveat:** This file is national only. State-level snapshots exist at `https://maps.glsen.org/state-research-snapshots/` (50 individual PDFs, not yet downloaded).

---

### 6.3 Williams Institute Health Reports

**Files:**
- `health/williams_health_medicaid_lgbtq_2025.pdf` — LGBTQ+ Medicaid coverage & access (2025)

**Key findings:** LGBTQ+ adults are more likely to be uninsured and to delay care due to cost. Transgender adults face particular barriers. State Medicaid expansion status intersects significantly with LGBTQ+ healthcare access.

**Use case:** Pair with HRC SEI healthcare ratings for a healthcare access composite layer.

---

### 6.4 CDC YRBSS SOGI Data

**File:** `youth/cdc_yrbss_sogi_2015_2017.csv` (9.0MB) — 50,000 rows

**Schema:**

| Column | Definition |
|--------|------------|
| `year` | Survey year (2015 or 2017) |
| `locationabbr` | State abbreviation or urban district code |
| `locationdesc` | Full location name |
| `topic` | Health topic category |
| `shortquestiontext` | Question summary |
| `greater_risk_data_value` | % reporting higher-risk behavior |
| `lesser_risk_data_value` | % reporting lower-risk behavior |
| `sample_size` | Number of respondents |
| `sexualidentity` | Bisexual / Gay or lesbian / Gay/lesbian/bisexual / Heterosexual (straight) / Not sure |

**Caveat:** This data is 2015–2017 only. More recent YRBSS cycles (2019, 2021, 2023) have SOGI data but require downloading the full YRBSS microdata files (~hundreds of MB per cycle). Trevor Project 2024 reports are more current and state-comprehensive for youth health context.

---

## 7. Economic Data

### 7.1 Williams Institute Economic PDFs

All four files are PDFs requiring table extraction. They provide LGBTQ+-specific economic data not available from Census:

| File | Key Data |
|------|----------|
| `economic/williams_economic_poverty_2019.pdf` | LGBT poverty rates by state, race, gender vs. non-LGBT |
| `economic/williams_economic_poverty_covid_2023.pdf` | Pandemic economic impact on LGBT adults |
| `economic/williams_economic_workplace_discrimination_2021.pdf` | Discrimination rates by identity type, industry |
| `economic/williams_economic_older_adults_2023.pdf` | Economic & health status of LGBT adults 50+ |

**Use case:** State comparison of LGBT poverty rates; workplace discrimination context. These numbers help explain economic disparities visible in Census data.

---

### 7.2 BLS Occupational Employment and Wages

**Status:** Manual download required. Instructions in `economic/BLS_OEWS_DOWNLOAD_INSTRUCTIONS.txt`.

Download `oesm24st.zip` from `https://www.bls.gov/oes/special.requests/oesm24st.zip` in a local browser and save as `economic/bls_oews_state_2024.zip`. The file of interest inside is `state_M2024_dl.xlsx`.

**Use case:** State-level occupational wage distributions as general economic baseline for comparison with LGBT economic data.

---

## 8. Community Infrastructure

### 8.1 IRS LGBTQ+ Nonprofits (NCCS BMF)

**File:** `community/irs_lgbtq_nonprofits_2026.csv` ⚠️ PARTIAL (~4,981 rows)

**Schema:**

| Column | Definition |
|--------|------------|
| `ein` | IRS Employer Identification Number (unique org ID) |
| `org_name_display` | Organization name |
| `org_addr_city` | City |
| `org_addr_state` | State (2-char) |
| `org_addr_zip5` | ZIP code |
| `ntee_code_clean` | NTEE major category code |
| `ntee_code_definition` | Human-readable NTEE category |
| `income_amount` | Annual income (USD) |
| `asset_amount` | Total assets (USD) |
| `revenue_amount` | Total revenue (USD) |

**Filter applied:** NTEE code P85 (LGBT organizations) OR org name contains: LGBT, LGBTQ, gay, lesbian, transgender, queer, bisexual, pride, same-sex.

**Caveat:** File is partial — download timed out at ~4,981 orgs. Full dataset likely has 5,000–8,000 orgs. Full re-run needed locally.

**Use case:** 
- Map layer of LGBTQ+ organization locations (needs geocoding by ZIP)
- "Community infrastructure density" metric per state/county
- Filter by NTEE to find health centers, advocacy orgs, youth orgs, etc.

**Geocoding:** ZIP code is available. Use Census ZIP-to-lat-lon crosswalk or geocoding API to place points on map.

---

## 9. Youth Data

Primary youth data: Trevor Project PDFs (Section 6.1) and CDC YRBSS CSV (Section 6.4).

No additional standalone youth CSV files. The Trevor Project PDFs are the most comprehensive and current (2024) state-level youth LGBTQ+ mental health resource in the dataset.

---

## 10. Socioeconomic & Household Profiles

### 10.1 Census ACS Supporting Tables

These provide general population context to benchmark against LGBTQ+-specific data:

| File | Coverage | Key Columns |
|------|----------|-------------|
| `socioeconomic/census_acs_B11001_state_2024.csv` | 52 states | `total_households`, `family_households`, `nonfamily_households`, `householder_living_alone`, `state_fips` |
| `socioeconomic/census_acs_B11001_county_2024.csv` | 3,222 counties | Same + `county_fips` |
| `socioeconomic/census_acs_B12001_state_2024.csv` | 52 states | `total_population_15plus`, `males_now_married`, `females_now_married`, `state_fips` |
| `socioeconomic/census_acs_B12001_county_2024.csv` | 3,222 counties | Same + `county_fips` |
| `socioeconomic/census_acs_B15002_state_2024.csv` | 52 states | `total_population_25plus`, `males_bachelors_degree`, `males_masters_degree`, `males_professional_degree`, `males_doctoral_degree`, `females_bachelors_degree`, `state_fips` |
| `socioeconomic/census_acs_B15002_county_2024.csv` | 3,222 counties | `total_population_25plus`, `males_bachelors_degree`, `state_fips`, `county_fips` |
| `socioeconomic/census_acs_S1101_state_2024.csv` | 52 states | `avg_household_size`, `avg_family_size`, `pct_households_with_children_under18`, `state_fips` |
| `socioeconomic/census_acs_S1501_state_2024.csv` | 52 states | `total_population_25plus`, `pct_bachelors_or_higher_female`, `pct_bachelors_or_higher_male`, `state_fips` |

**Use case:** Normalize LGBTQ+ data against general population baselines. E.g., same-sex couples as % of all couples; LGBTQ+ nonprofits per 100k residents.

---

### 10.2 Williams Institute Socioeconomic PDFs

| File | Key Content |
|------|-------------|
| `socioeconomic/williams_socioeconomic_married_couples_2025.pdf` | 10 years of same-sex marriage data post-Obergefell; state trends |
| `socioeconomic/williams_socioeconomic_economic_impact_marriage_2025.pdf` | Economic impact of marriage equality ($3.8B+ in wedding spending, etc.) |
| `socioeconomic/williams_socioeconomic_race_comparison_2022.pdf` | Race/ethnicity composition of LGBT adults by state |
| `socioeconomic/williams_socioeconomic_black_lgbt_2021.pdf` | Demographics, health, and economic profile of Black LGBT adults |
| `socioeconomic/williams_socioeconomic_education_college_2022.pdf` | Education attainment comparison; student debt |
| `socioeconomic/williams_socioeconomic_trans_nonbinary_lacounty_2024.pdf` | Deep dive on trans/nonbinary adults in LA County (model for other cities) |

---

### 10.3 ACS PUMS Data Dictionary

**File:** `socioeconomic/census_pums_data_dictionary_2024.pdf`

Reference document for the ACS Public Use Microdata Sample. The PUMS files themselves (multi-GB) are not downloaded but are the backbone of any LGBTQ+-specific income, occupation, or education analysis. Key PUMS variables for LGBTQ+ analysis:
- `RELSHIPP` / `Erelatp` — Relationship to householder (codes for same-sex spouse, unmarried partner)
- `PARTNER` — Unmarried partner indicator
- `SEX` — Sex (2024 PUMS added non-binary option)
- `AGEP` — Age
- `PINCP` — Personal income
- `POVPIP` — Income-to-poverty ratio
- `OCCP` — Occupation code
- `NAICSP` — Industry code
- `SCHL` — Educational attainment

---

## 11. Geographic Reference Files

All in `geo/`. These are the base layers for all map visualizations.

| File | Scale | Use |
|------|-------|-----|
| `census_state_boundaries_500k.zip` | 1:500k | State polygons (default choropleth layer) |
| `census_state_boundaries_5m.zip` | 1:5M | Simplified state polygons (overview/thumbnail maps) |
| `census_county_boundaries_500k.zip` | 1:500k | County polygons (county choropleth layer) |
| `census_cbsa_boundaries_500k.zip` | 1:500k | Core Based Statistical Areas (metro area layer) |
| `census_fips_state.txt` | — | State FIPS codes crosswalk |
| `census_fips_county.txt` | — | County FIPS codes crosswalk |

**Format:** All boundary files are ZIP archives containing ESRI Shapefiles (.shp, .dbf, .prj, .shx). Convert to GeoJSON for web use:
```bash
ogr2ogr -f GeoJSON state_boundaries.geojson /path/to/cb_2022_us_state_500k.shp
```
Or use a library like `geopandas` (Python) or `mapshaper` for conversion and simplification.

**Join key:** All Census data files include `state_fips` (2-char). Shapefiles use `STATEFP` for states, `STATEFP`+`COUNTYFP` for counties. The 5-char combined FIPS (`state_fips + county_fips`) matches shapefile `GEOID`.

---

## 12. Join Keys & Data Relationships

### Primary Join Keys

| Dataset A | Dataset B | Join Key | Notes |
|-----------|-----------|----------|-------|
| Census CSVs | State boundaries | `state_fips` (2-char) = shapefile `STATEFP` | Direct match |
| Census county CSVs | County boundaries | `state_fips + county_fips` (5-char) = shapefile `GEOID` | Concatenate for join |
| FBI hate crime CSV | Census state | `state_abbr` → `state_fips` via FIPS table | Need crosswalk |
| HRC SEI (extracted) | Census state | `state_abbr` → `state_fips` | Need crosswalk |
| Trans leg. tracker | Census state | `state` (name) → `state_fips` | Name match |
| HRC MEI cities | State boundaries | `state` (2-char abbr) | City-level; need geocoding for lat/lon |
| LGBTQ+ nonprofits | County/state | `org_addr_state`, `org_addr_zip5` | ZIP geocoding needed |
| Trevor Project (extracted) | State boundaries | `state_abbr` | After PDF extraction |

### State FIPS/Abbreviation Crosswalk

The file `geo/census_fips_state.txt` (pipe-delimited) maps between FIPS codes and state abbreviations. Use this as a lookup table whenever joining datasets that use different state identifiers.

### Computing Rates (Normalization)

For any per-capita or rate calculation, join to the Williams Institute population estimates (Section 3.2) or use `total_households` from B11001 as a denominator.

**Example — hate crime rate:**
```
lgbtq_hate_crime_rate_per_100k = (total_lgbtq_incidents / state_adult_population) × 100,000
```

---

## 13. Files Requiring Manual Extraction

These PDFs contain structured data that must be extracted before the app can use them. Priority order:

### Priority 1 — Trevor Project State Data
Extract from all 50 state PDFs: `health/trevorproject_survey_2024_{State}.pdf`
**Target:** `health/trevorproject_survey_2024_extracted.csv`
**Method:** PyMuPDF (`fitz`) or `pdfplumber` — the tables are consistently formatted across all 50 PDFs. A single extraction script with pattern matching should handle all 50.

### Priority 2 — HRC State Equality Index
Extract from: `legal/hrc_sei_2024_national_scorecard.pdf`
**Target:** `legal/hrc_sei_2024_extracted.csv`
**Method:** The scorecard is a formatted table; pdfplumber or manual transcription (50 rows).

### Priority 3 — Williams Institute Population Estimates
Extract from: `population/williams_population_estimates_2023.pdf`
**Target:** `population/williams_population_estimates_extracted_2023.csv`
**Method:** Table extraction — state-by-state population percentages.

### Priority 4 — HRC CEI Appendix A Company Scores
Extract from: `legal/hrc_cei_2025_appendix_a_companies.pdf`
**Target:** `legal/hrc_cei_2025_companies_extracted.csv`
**Method:** Table extraction — company name + score columns.

### Priority 5 — HRC SEI Issue Brief & Williams Institute Economic PDFs
These contain narrative statistics rather than clean tables. Manual extraction of key statistics for use in UI copy/tooltips.

---

## 14. Known Data Gaps

Items not yet collected that would meaningfully improve the app:

| Gap | Why It Matters | Source |
|-----|----------------|--------|
| CDC HIV surveillance (state-level, MSM) | HIV disparities among gay/bisexual men | `https://gis.cdc.gov/grasp/nchhstpatlas/main.html` |
| MAP state policy scorecard 2025 | More granular than HRC SEI; numerical scores per policy category | `https://www.lgbtmap.org/equality-maps` |
| Census PUMS microdata (1yr + 5yr) | Income, poverty, occupation for same-sex couples | 3–15GB; local download required |
| GLSEN state snapshots (all 50) | School climate per state | 50 PDFs at maps.glsen.org |
| BLS OEWS state wage data | Occupational wage baselines by state | Local download; see instructions file |
| Victory Fund elected officials | Count of openly LGBTQ+ officeholders by state | victoryfund.org |
| ACLU legislative tracker 2025 | Bill-by-bill tracking with status | aclu.org |
| CDC NHIS adult SOGI (2024) | Health insurance, conditions, access by LGBTQ+ identity | cdc.gov/nchs/nhis |
| HRC HEI facility-level data | Geocoded LGBTQ+-affirming hospitals/clinics | Requires HRC data request |
| Full IRS nonprofit re-run | ~4,981 of ~8,000 orgs captured | Local download of 1.7GB source |

---

## 15. Critical Display Caveats

**Always display these warnings/disclaimers in the UI where relevant:**

### Hate Crime Data
> "FBI hate crime statistics reflect only incidents reported to law enforcement agencies that participate in hate crime reporting. Many jurisdictions do not submit data, and hate crimes are significantly underreported. These figures represent a minimum floor — the actual number of hate crimes is higher. Additionally, a jurisdiction reporting zero incidents may mean zero crimes occurred, or that the jurisdiction does not track or report hate crimes. Do not compare raw counts between states without accounting for reporting participation rates."

### ACS Same-Sex Household Counts
> "Census Bureau data on same-sex households counts married and cohabiting couples only. It does not include LGBTQ+ individuals who live alone, with non-romantic roommates, or with family members. The actual LGBTQ+ population is substantially larger than these household counts suggest."

### Trevor Project Survey
> "Survey data is self-selected and reflects experiences of LGBTQ+ youth who participated in the Trevor Project survey. Findings may not be representative of all LGBTQ+ youth in each state."

### MEI Scores
> "Municipal Equality Index scores reflect city policies and laws, not necessarily the lived experiences of LGBTQ+ residents. A high score indicates protective policies exist; it does not guarantee freedom from discrimination or harassment. Scores are updated annually and reflect the year indicated."

### Gallup State Data
> "State-level LGBTQ+ identification data from Gallup requires a subscription and is not included in this dataset. National estimates and generational breakdowns are shown instead."

### PDF-Extracted Data
> "Data extracted from PDF reports may contain transcription errors. Verify key figures against original source documents."

---

*This reference document covers data as downloaded through 2026-04-27. Check individual source URLs for more recent releases.*
