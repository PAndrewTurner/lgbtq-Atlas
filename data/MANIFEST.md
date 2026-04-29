# LGBTQ+ Atlas — Data Manifest

**Generated:** 2026-04-27  
**Last updated:** 2026-04-27  
**Maintainer:** LGBTQ+ Atlas Project  
**Purpose:** Documents every file in `data/raw/`, including source URL, download date, vintage year, coverage, and caveats.  
**Total files:** 105 | **Total size:** ~187MB

---

## STATUS LEGEND
- ✅ **DOWNLOADED** — File is present and ready for pipeline
- ⚠️ **PARTIAL** — File present but incomplete; see caveats
- 🔲 **MANUAL DOWNLOAD REQUIRED** — File requires browser interaction or registration
- 📋 **PLACEHOLDER** — File contains HTML or instructions, not data

---

## 1. POPULATION & DEMOGRAPHICS (`data/raw/population/`)

### census_acs_B11009_state_2024.csv
- **Source:** U.S. Census Bureau — American Community Survey 5-Year
- **URL:** `https://api.census.gov/data/2024/acs/acs5?get=NAME,B11009_*&for=state:*`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024 | **Published:** December 2025
- **Coverage:** All 50 states + DC (52 rows)
- **Columns:** `geography`, `total_households`, `married_couple_households`, `opposite_sex_married_households`, `same_sex_married_households`, `male_male_married_households`, `female_female_married_households`, `cohabiting_couple_households`, `opposite_sex_cohabiting_households`, `same_sex_cohabiting_households`, `male_male_cohabiting_households`, `female_female_cohabiting_households`, `all_other_households`, `state_fips`
- **Caveats:** ACS 5-year estimates. Since 2019, Census directly asks about same-sex relationships.
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED

### census_acs_B11009_state_2024_1yr.csv
- **Source:** U.S. Census Bureau — ACS 1-Year
- **URL:** `https://api.census.gov/data/2024/acs/acs1?get=NAME,B11009_*&for=state:*`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024 | **Published:** September 2025
- **Coverage:** All 50 states + DC (52 rows) — only states with large enough samples reliable
- **Columns:** Same as B11009 5-year above
- **Caveats:** Higher margins of error than 5-year; prefer 5-year for small states
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED

### census_acs_B11009_county_2024.csv
- **Source:** U.S. Census Bureau — ACS 5-Year
- **URL:** `https://api.census.gov/data/2024/acs/acs5?get=NAME,B11009_*&for=county:*`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024
- **Coverage:** 3,222 counties/county equivalents
- **Columns:** Same as B11009 state above, plus `county_fips`
- **Caveats:** Counties with small same-sex household counts may have suppressed data
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED

### williams_population_estimates_2023.pdf
- **Source:** Williams Institute, UCLA School of Law
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/LGBT-Adult-US-Pop-Dec-2023.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2023 data | **Published:** December 2023
- **Coverage:** All 50 states + DC; breakdowns by gender identity, race/ethnicity, age, urban/rural
- **Key variables:** LGBT population count and % of adult population by state; LGB vs. transgender; race/ethnicity; age groups
- **Caveats:** Most recent as of April 2026. No direct CSV — extract tables into `williams_population_estimates_extracted_2023.csv`
- **Update cadence:** ~Annual | **Status:** ✅ DOWNLOADED (PDF) | 🔲 Manual table extraction needed

---

## 2. LEGAL & POLICY CLIMATE (`data/raw/legal/`)

### hrc_mei_city_scores_2025.csv ✅ NEW
- **Source:** Human Rights Campaign — Municipal Equality Index, municipality database
- **URL:** `https://www.hrc.org/resources/municipalities/search?q=` (scraped all 51 paginated pages via browser automation)
- **Downloaded:** 2026-04-27 | **Vintage:** 2025 MEI edition
- **Coverage:** 506 cities/municipalities across all 50 states
- **Columns:** `city`, `state`, `mei_score` (0–100), `hrc_slug` (URL path for detail page)
- **Key stats:** 132 perfect (100-point) cities; mean score 70.1; range 0–100
- **Caveats:** Scores reflect overall MEI composite. Subcategory breakdowns (Non-Discrimination Laws, Municipality as Employer, Municipal Services, Law Enforcement, Leadership on LGBTQ+) require visiting individual city pages. Data accurate as of scrape date.
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED

### hrc_mei_2025.pdf
- **Source:** Human Rights Campaign — Municipal Equality Index 2025
- **URL:** `https://reports.hrc.org/municipal-equality-index-2025`
- **Downloaded:** 2026-04-27 | **Vintage:** 2025 | **Size:** 313KB
- **Coverage:** 506 U.S. cities rated on 49 criteria across 5 categories
- **Key variables:** City score (0–100); non-discrimination laws, municipal services, law enforcement, city leadership, relationship recognition
- **Caveats:** City-level CSV not publicly available; contact `mei@hrc.org`. Historical back to 2021.
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED (PDF) | 🔲 CSV requires manual compilation

### hrc_mei_2024.pdf
- **Source:** Human Rights Campaign — Municipal Equality Index 2024
- **URL:** `https://reports.hrc.org/municipal-equality-index-2024`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024 | **Size:** 320KB
- **Coverage:** 506 U.S. cities (prior year for year-over-year comparison)
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED

### hrc_sei_2024_national_scorecard.pdf
- **Source:** Human Rights Campaign — State Equality Index 2024, National Scorecard
- **URL:** `https://hrc-prod-requests.s3-us-west-2.amazonaws.com/files/documents/SEI-2024-National-Scorecard.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024 | **Size:** 347KB
- **Coverage:** All 50 states rated across four policy categories
- **Key variables:** State-level ratings (High, Medium, Low, Negative) for: relationship/parental recognition, non-discrimination protections, religious exemptions, healthcare/safety laws; overall climate rating per state
- **Caveats:** Full SEI report is browser-accessible at `https://reports.hrc.org/2024-state-equality-index`. State ratings are the primary quantifiable output — extract into a CSV for cross-state analysis.
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED

### hrc_sei_2024_issue_brief.pdf
- **Source:** Human Rights Campaign — State Equality Index 2024, Issue Brief
- **URL:** `https://hrc-prod-requests.s3-us-west-2.amazonaws.com/files/documents/SEI24_IssueBrief.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024 | **Size:** 197KB
- **Coverage:** National; summary of anti-LGBTQ+ legislative trends and state climate shifts
- **Status:** ✅ DOWNLOADED

### hrc_hei_2024_executive_summary.pdf
- **Source:** Human Rights Campaign — Healthcare Equality Index 2024, Executive Summary
- **URL:** `https://hrc-prod-requests.s3-us-west-2.amazonaws.com/HEI-2024-Executive-Summary.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024 | **Size:** 5.0MB
- **Coverage:** 1,065+ U.S. healthcare facilities rated on LGBTQ+ patient care policies
- **Key variables:** Facility score (0–100); categories: non-discrimination patient care, visitor policies, employment non-discrimination, training, transgender-inclusive care
- **Caveats:** Facility-level data not available as CSV. Full HEI report and facility directory at `https://www.hrc.org/resources/healthcare-equality-index`. Useful for mapping LGBTQ+-affirming healthcare access by geography.
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED (executive summary)

### hrc_cei_2025_corporate_citizens.pdf
- **Source:** Human Rights Campaign — Corporate Equality Index 2025, Corporate Citizens Report
- **URL:** `https://hrc-prod-requests.s3-us-west-2.amazonaws.com/LGBTQ-Corporate-Citizen-Report-12524.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2025 | **Size:** 6.6MB
- **Coverage:** 1,300+ major U.S. employers rated on LGBTQ+ workplace policies
- **Key variables:** Company score (0–100); categories: workforce protections, inclusive benefits (domestic partner, transgender healthcare), supporting inclusive culture, corporate citizenship/responsible giving
- **Caveats:** Employer-level data also in Appendix A (see below). Useful for economic/workplace analysis — cross-reference employer headquarters locations with state-level LGBTQ+ climate.
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED

### hrc_cei_2025_appendix_a_companies.pdf
- **Source:** Human Rights Campaign — Corporate Equality Index 2025, Appendix A (Full Company Scores)
- **URL:** `https://hrc-prod-requests.s3-us-west-2.amazonaws.com/Report-Design-Graphics/CEI-images/CEI-2024/CEI-2025-Appendix-A-Company-7.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2025 | **Size:** 1.1MB
- **Coverage:** Complete alphabetical list of all rated companies with scores and ratings
- **Caveats:** Extract company + score table into `hrc_cei_2025_companies_extracted.csv` for analysis
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED

### trans_legislation_tracker_2025_state.csv
- **Source:** Trans Legislation Tracker — translegislation.com
- **URL:** `https://translegislation.com/bills/2025`
- **Downloaded:** 2026-04-27 | **Vintage:** 2025 session (through April 2026)
- **Coverage:** 49 states + federal — 1,022 total bills tracked
- **Key variables:** `state`, `bills_introduced_2025`, `year`, `source`
- **Caveats:** Extracted from Next.js `__NEXT_DATA__` JSON — state totals only, not individual bills
- **Update cadence:** Continuous | **Status:** ✅ DOWNLOADED

### trans_legislation_tracker_2025_categories.csv
- **Source:** Trans Legislation Tracker — translegislation.com
- **Downloaded:** 2026-04-27 | **Vintage:** 2025 session
- **Coverage:** National; 20 bill categories. Top: education (280), healthcare (214), other (174), sports (127)
- **Update cadence:** Continuous | **Status:** ✅ DOWNLOADED

### trans_legislation_tracker_national_trend.csv
- **Source:** Trans Legislation Tracker — translegislation.com
- **Downloaded:** 2026-04-27 | **Vintage:** 2023–2025
- **Coverage:** 2023 (615 bills, 87 passed), 2024 (701 bills, 51 passed), 2025 (1,022 bills, 126 passed)
- **Status:** ✅ DOWNLOADED

### fbi_hatecrimes_lgbtq_2019_2024.csv ✅ NEW
- **Source:** FBI Crime Data Explorer API (`cde.ucr.cjis.gov/LATEST/hate-crime/`)
- **URL pattern:** `https://cde.ucr.cjis.gov/LATEST/hate-crime/state/{STATE}/?from=01-{YEAR}&to=12-{YEAR}&type=totals`
- **Downloaded:** 2026-04-27 | **Vintage:** 2019–2024
- **Coverage:** National + all 50 states + DC × 5 years = 260 rows
- **Columns:** `geography`, `state_abbr`, `year`, `anti_gay_male`, `anti_lesbian_female`, `anti_lgbtq_mixed`, `anti_transgender`, `anti_gender_nonconforming`, `anti_bisexual`, `total_lgbtq_incidents`, `total_sexual_orientation`, `total_gender_identity`, `total_all_hate_crimes`
- **Key findings:** National LGBTQ+ hate crime incidents rose 89% from 2019 (1,537) to 2023 (2,899). Anti-Gay (Male) and Anti-Transgender are the largest subcategories. Top states in 2023: CA (527), NJ (233), WA (192), NY (168), MA (158).
- **Caveats:** Counts reflect incidents reported to the FBI. Significant underreporting is known — many jurisdictions do not submit hate crime data and those that do vary in recording practices. These figures represent a floor, not a ceiling. Do not compare raw state counts without normalizing for reporting participation. NIBRS transition (ongoing 2021–2023) also affects year-over-year comparability.
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED (2019–2024 via CDE API)

### fbi_hatecrimes_all_2024.csv
- **Note:** This file contains an HTML placeholder — the CDE browser interface does not support programmatic download. The API dataset above (`fbi_hatecrimes_lgbtq_2019_2024.csv`) supersedes this file for analysis purposes.
- **Status:** 📋 PLACEHOLDER — superseded by API-downloaded CSV above

### FBI_DOWNLOAD_INSTRUCTIONS.txt
- **Status:** ✅ Instructions for manual download of full agency-level FBI hate crime data

**Additional legal sources needed (manual):**
- `map_state_policy_scorecard_2025.csv` — MAP Equality Maps; `https://www.lgbtmap.org/equality-maps`
- `aclu_legislation_tracker_2025.csv` — `https://www.aclu.org/legislative-attacks-on-lgbtq-rights`
- `victory_fund_officials_2025.csv` — `https://victoryfund.org/our-candidates/`

---

## 3. SAFETY DATA (`data/raw/safety/`)

### fbi_hatecrimes_lgbtq_2019_2024.csv
- See full entry under Legal section above.
- **Status:** ✅ DOWNLOADED — 312 rows, national + all 50 states + DC, 2019–2024

### fbi_hatecrimes_all_2024.csv
- HTML placeholder — superseded by the API-downloaded CSV above.
- **Status:** 📋 PLACEHOLDER

### FBI_DOWNLOAD_INSTRUCTIONS.txt
- **Status:** ✅ Instructions present

**Additional safety sources needed:**
- `ncavp_hateviolence_[year].pdf` — NCAVP/AVP annual LGBTQ+ hate violence report. `https://avp.org/ncavp/`

---

## 4. HEALTH & WELLBEING (`data/raw/health/`)

### trevorproject_survey_2024.pdf
- **Source:** The Trevor Project — 2024 National Survey on LGBTQ Youth Mental Health
- **URL:** `https://www.thetrevorproject.org/wp-content/uploads/2025/02/2024-50-State-Report.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024 survey | **Published:** February 2025 | **Size:** 7.4MB
- **Coverage:** National + all 50 states; 18,000+ LGBTQ+ youth ages 13–24
- **Key variables:** Suicidality rates, mental health support access, conversion therapy exposure, school safety, family acceptance
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED

### trevorproject_survey_2024_[State].pdf — All 50 States
- **Source:** The Trevor Project — 2024 State-Level Reports
- **URL pattern:** `https://www.thetrevorproject.org/wp-content/uploads/2025/02/2024-50-State-Report-[StateName].pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024 | **Size:** ~1.8MB each | **Total:** ~90MB
- **Coverage:** All 50 states. Multi-word states use CamelCase in URL (e.g., `NewYork`, `NorthCarolina`). Washington state used for DC equivalent.
- **States present:** Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, NewHampshire, NewJersey, NewMexico, NewYork, NorthCarolina, NorthDakota, Ohio, Oklahoma, Oregon, Pennsylvania, RhodeIsland, SouthCarolina, SouthDakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, WestVirginia, Wisconsin, Wyoming
- **Caveats:** Extract key metrics (suicidality %, mental health access %, conversion therapy exposure %) into `trevorproject_survey_2024_extracted.csv` for analysis
- **Status:** ✅ DOWNLOADED (all 50 states)

### glsen_nscs_2024_toolkit.pdf
- **Source:** GLSEN — 2024 National School Climate Survey
- **URL:** `https://assets-us-01.kc-usercontent.com/0234f496-d2b7-00b6-17a4-b43e949b70a2/327f82f9-afef-4149-9e0c-ce11276cc4af/GLSEN%202024%20National%20School%20Climate%20Survey+Toolkit.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2023–2024 school year | **Size:** 1.7MB
- **Coverage:** National; LGBTQ+ students ages 13+ at U.S. secondary schools
- **Key variables:** % feeling unsafe, GSA club presence, anti-bullying policy coverage, LGBTQ+ curriculum inclusion
- **Caveats:** State-level snapshots at `https://maps.glsen.org/state-research-snapshots/` — individual PDFs per state (50 downloads needed)
- **Update cadence:** ~Every 2 years | **Status:** ✅ DOWNLOADED (national PDF)

### williams_health_medicaid_lgbtq_2025.pdf
- **Source:** Williams Institute, UCLA School of Law
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/LGBTQ-Medicaid-Coverage-Jan-2025.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2025 | **Size:** 2.3MB
- **Coverage:** National; LGBTQ+ adults' Medicaid coverage and access
- **Update cadence:** ~Annual | **Status:** ✅ DOWNLOADED

**Additional health sources needed (manual download):**
- `cdc_brfss_sogi_[year].csv` — CDC BRFSS SOGI module. `https://chronicdata.cdc.gov` — search "BRFSS SOGI". Note: CDC Socrata portal has YRBSS SOGI data (2015–2017, dataset `q6p7-56au`) but not a dedicated BRFSS SOGI module via API. BRFSS SOGI data may require direct BRFSS data file download from `https://www.cdc.gov/brfss/annual_data/annual_data.htm`.
- `cdc_hiv_atlas_[year].csv` — CDC NCHHSTP Atlas. `https://gis.cdc.gov/grasp/nchhstpatlas/main.html` — requires browser interaction. Key: HIV diagnoses by state × transmission category (MSM).
- `kff_lgbtq_health_[year].pdf` — KFF LGBTQ+ Health Policy brief. `https://www.kff.org/other/issue-brief/health-and-access-to-care-and-coverage-for-lesbian-gay-bisexual-and-transgender-individuals-in-the-u-s/`
- `nhis_adult_2024.csv` — CDC NHIS Adult Sample Person file with SOGI variables. `https://www.cdc.gov/nchs/nhis/data-questionnaires-documentation.htm`

---

## 5. ECONOMIC DATA (`data/raw/economic/`)

### williams_economic_poverty_2019.pdf
- **Source:** Williams Institute — "LGBT Poverty in the United States"
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/National-LGBT-Poverty-Oct-2019.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2019 | **Size:** 4.7MB
- **Coverage:** National; LGBT poverty rates vs. non-LGBT, by race, gender, state
- **Update cadence:** Periodically | **Status:** ✅ DOWNLOADED

### williams_economic_poverty_covid_2023.pdf
- **Source:** Williams Institute — "COVID-19 and LGBT Economic Hardship"
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/LGBT-COVID-Poverty-Oct-2023.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2023 | **Size:** 2.5MB
- **Coverage:** National; pandemic-era economic impacts on LGBT adults
- **Status:** ✅ DOWNLOADED

### williams_economic_workplace_discrimination_2021.pdf
- **Source:** Williams Institute — "LGBT People's Experiences of Workplace Discrimination and Harassment"
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/Workplace-Discrimination-Sep-2021.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2021 | **Size:** 3.0MB
- **Coverage:** National; rates of workplace discrimination by identity type, race, industry
- **Status:** ✅ DOWNLOADED

### williams_economic_older_adults_2023.pdf
- **Source:** Williams Institute — "LGBT Older Adults in Long-Term Care Facilities"
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/LGBT-Older-Adults-LTC-Aug-2023.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2023 | **Size:** 3.2MB
- **Coverage:** National; economic and health status of LGBT adults 50+
- **Status:** ✅ DOWNLOADED

### BLS_OEWS_DOWNLOAD_INSTRUCTIONS.txt
- **Source:** U.S. Bureau of Labor Statistics — Occupational Employment and Wage Statistics
- **Target URL:** `https://www.bls.gov/oes/special.requests/oesm24st.zip`
- **Vintage:** May 2024 | **Published:** March 2025
- **Coverage:** State-level occupational employment and annual mean wages
- **Caveats:** BLS blocks programmatic downloads from cloud/server IPs (confirmed 403 on all attempts). Download from local browser and save as `bls_oews_state_2024.zip`. After unzipping keep `state_M2024_dl.xlsx`.
- **Status:** 📋 MANUAL DOWNLOAD REQUIRED — see instructions file

**Additional economic sources needed (large files — manual/local download):**
- `census_pums_2024_1yr_person.csv` — ACS PUMS 1-year person file (~3GB). `https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/` → `csv_pus.zip`
- `census_pums_2024_5yr_person.csv` — ACS PUMS 5-year person file (~15GB). Same path but `5-Year/`
- `census_pums_2024_1yr_household.csv` — ACS PUMS 1-year household file. Same dir → `csv_hus.zip`
- `census_pums_2024_5yr_household.csv` — ACS PUMS 5-year household file
- `hud_lgbtq_housing_[year].csv` — HUD housing discrimination data. `https://www.huduser.gov/portal/datasets/hsg_discrimination.html`

---

## 6. COMMUNITY INFRASTRUCTURE (`data/raw/community/`)

### irs_lgbtq_nonprofits_2026.csv
- **Source:** NCCS / Urban Institute — Business Master File (BMF) filtered for LGBTQ+ organizations
- **URL:** `https://nccsdata.s3.us-east-1.amazonaws.com/processed/bmf/2026_01/bmf_2026_01_processed.csv`
- **Downloaded:** 2026-04-27 | **Vintage:** January 2026 BMF
- **Coverage:** ~4,981 LGBTQ+-related 501(c)(3) organizations (partial — see caveats)
- **Key variables:** `ein`, `org_name_display`, `org_addr_city`, `org_addr_state`, `org_addr_zip5`, `ntee_code_clean`, `ntee_code_definition`, `income_amount`, `asset_amount`, `revenue_amount`
- **Filter applied:** NTEE code P85 OR org name contains: LGBT, LGBTQ, gay, lesbian, transgender, queer, bisexual, pride, same-sex
- **Caveats:** ⚠️ PARTIAL — source is 1.7GB; download timed out mid-stream. Full re-run will yield ~5,000–8,000 orgs. Download full file locally and refilter.
- **Update cadence:** Monthly | **Status:** ⚠️ PARTIAL

### nccs_bmf_data_dictionary_2026_01.csv
- **Source:** NCCS / Urban Institute
- **URL:** `https://nccsdata.s3.us-east-1.amazonaws.com/processed/bmf/2026_01/bmf_2026_01_data_dictionary.csv`
- **Downloaded:** 2026-04-27 | **Size:** 6.9KB
- **Coverage:** Field definitions for BMF processed file
- **Status:** ✅ DOWNLOADED

**Additional community sources needed (manual):**
- `pride_events_compiled_2025.csv` — Manual compile from Wikipedia, Eventbrite, InterPride (`https://interpride.org`)
- `glsen_state_snapshot_[state]_2024.pdf` — 50 per-state PDFs. `https://maps.glsen.org/state-research-snapshots/`

---

## 7. YOUTH DATA (`data/raw/youth/`)

### cdc_yrbss_sogi_2015_2017.csv
- **Source:** CDC DASH — Youth Risk Behavior Surveillance System (YRBSS), High School, Including Sexual Orientation
- **URL:** `https://data.cdc.gov/resource/q6p7-56au.csv` (Socrata API, dataset ID `q6p7-56au`)
- **Downloaded:** 2026-04-27 | **Vintage:** 2015 and 2017 survey years | **Size:** 9.0MB
- **Coverage:** 50,000 rows; 61 U.S. locations (states + large urban school districts); LGBTQ+ youth stratified by sexual identity
- **Key variables:** `year`, `locationabbr`, `locationdesc`, `topic`, `shortquestiontext`, `greater_risk_data_value`, `lesser_risk_data_value`, `sample_size`, `sexualidentity`
- **Sexual identity values:** Bisexual, Gay or lesbian, Gay/lesbian/bisexual, Heterosexual (straight), Not sure
- **Topics covered:** Unintentional injuries/violence, dietary behaviors, tobacco use, alcohol/drugs, sexual behaviors, physical activity, obesity/weight, other health
- **Caveats:** This CDC dataset covers 2015–2017 only (SOGI module was optional; not all states participated every cycle). More recent YRBSS SOGI data requires downloading raw YRBSS files from `https://www.cdc.gov/yrbs/data/index.htm`. The 50k-row API limit was hit; full dataset has 6.2M rows (all breakouts). This file filtered for `sexualidentity != Total`, `race = Total`, `grade = Total`, `sex = Total`.
- **Update cadence:** Biennial | **Status:** ✅ DOWNLOADED (2015–2017 SOGI subset)

**Primary youth data source:** Trevor Project 2024 state reports — see Health section (all 50 states downloaded).

---

## 8. SOCIOECONOMIC & HOUSEHOLD PROFILES (`data/raw/socioeconomic/`)

### census_acs_B11001_state_2024.csv / census_acs_B11001_county_2024.csv
- **Source:** Census Bureau ACS 5-Year 2024 — Household Type
- **Downloaded:** 2026-04-27 | **Coverage:** State (52 rows) and county (3,222 rows)
- **Columns:** `geography`, `total_households`, `family_households`, `nonfamily_households`, `householder_living_alone`, `state_fips` (+ `county_fips` for county file)
- **Status:** ✅ DOWNLOADED (both)

### census_acs_B12001_state_2024.csv / census_acs_B12001_county_2024.csv
- **Source:** Census Bureau ACS 5-Year 2024 — Sex by Marital Status
- **Downloaded:** 2026-04-27 | **Coverage:** State (52) and county (3,222)
- **Columns:** `geography`, `total_population_15plus`, `males_now_married`, `females_now_married`, `state_fips` (+ `county_fips` for county file)
- **Status:** ✅ DOWNLOADED (both)

### census_acs_B15002_state_2024.csv
- **Source:** Census Bureau ACS 5-Year 2024 — Sex by Educational Attainment
- **Downloaded:** 2026-04-27 | **Coverage:** State (52)
- **Columns:** `geography`, `total_population_25plus`, `males_bachelors_degree`, `males_masters_degree`, `males_professional_degree`, `males_doctoral_degree`, `females_bachelors_degree`, `state_fips`
- **Caveats:** General population baseline; pair with Williams Institute education reports for LGBTQ+ comparison
- **Status:** ✅ DOWNLOADED

### census_acs_B15002_county_2024.csv
- **Source:** Census Bureau ACS 5-Year 2024 — Sex by Educational Attainment
- **Downloaded:** 2026-04-27 | **Coverage:** County (3,222)
- **Columns:** `geography`, `total_population_25plus`, `males_bachelors_degree`, `state_fips`, `county_fips`
- **Caveats:** County pull captured fewer education variables than state; re-pull with full variable list if deeper breakdown needed
- **Status:** ✅ DOWNLOADED

### census_acs_S1101_state_2024.csv
- **Source:** Census Bureau ACS 5-Year 2024 Subject Table — Households and Families
- **Downloaded:** 2026-04-27 | **Coverage:** 52 states/DC
- **Columns:** `geography`, `avg_household_size`, `avg_family_size`, `pct_households_with_children_under18`, `state_fips`
- **Caveats:** County-level requires state-by-state API calls (subject tables don't support `for=county:*`)
- **Status:** ✅ DOWNLOADED

### census_acs_S1501_state_2024.csv
- **Source:** Census Bureau ACS 5-Year 2024 Subject Table — Educational Attainment
- **Downloaded:** 2026-04-27 | **Coverage:** 52 states/DC
- **Columns:** `geography`, `total_population_25plus`, `pct_bachelors_or_higher_female`, `pct_bachelors_or_higher_male`, `state_fips`
- **Status:** ✅ DOWNLOADED

### census_pums_data_dictionary_2024.pdf
- **Source:** U.S. Census Bureau — ACS PUMS Data Dictionary 2024
- **URL:** `https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2024.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024 | **Size:** 386KB
- **Coverage:** Variable definitions, codes, and response categories for all ACS PUMS variables including Erelatp (relationship), PARTNER (unmarried partner), SEX, AGEP, RAC1P, HISP, SCHL, OCCP, NAICSP, PINCP, POVPIP, etc.
- **Caveats:** Reference document — use to identify which PUMS variable codes correspond to same-sex couples, unmarried partners, non-binary gender (added 2024), etc.
- **Status:** ✅ DOWNLOADED

### gallup_lgbtq_demographics_2024.csv
- **Source:** Gallup — "LGBTQ+ Identification in U.S. Ticks Up to 9.3%" (February 2025)
- **URL:** `https://news.gallup.com/poll/656708/lgbtq-identification-rises.aspx`
- **Downloaded:** 2026-04-27 (manually compiled from published article) | **Vintage:** 2024 survey
- **Coverage:** National; breakdowns by generation and identity type
- **Key variables:** `category`, `group`, `lgbtq_pct`, `year`, `source`
- **Key findings:** 9.3% of U.S. adults identify as LGBTQ+; Gen Z 22.3%, Millennials 11.5%, Gen X 5.6%, Boomers 2.5%; Bisexual 4.5%, Gay/Lesbian 2.2%, Transgender 1.1%
- **Caveats:** State-level data requires Gallup subscription
- **Update cadence:** Annual | **Status:** ✅ DOWNLOADED (national summary)

### gallup_lgbtq_national_trend_2012_2024.csv
- **Source:** Gallup annual LGBT identification surveys
- **Downloaded:** 2026-04-27 | **Vintage:** 2012–2024 (8 data points)
- **Coverage:** 3.5% (2012) → 9.3% (2024) national trend
- **Status:** ✅ DOWNLOADED

### williams_socioeconomic_married_couples_2025.pdf
- **Source:** Williams Institute — "10 Years After Obergefell: Same-Sex Married Couples in the U.S."
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/Same-Sex-Marriage-Jun-2025.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2025 | **Size:** 4.7MB
- **Coverage:** National + state; same-sex married couple demographics, 10-year trend since Obergefell
- **Status:** ✅ DOWNLOADED

### williams_socioeconomic_economic_impact_marriage_2025.pdf
- **Source:** Williams Institute — "The Economic Impact of Marriage Equality: 10 Years After Obergefell"
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/Obergefell-Economic-Impact-Jun-2025.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2025 | **Size:** 2.1MB
- **Coverage:** National economic impact; wedding industry, healthcare, spending, tax revenue
- **Status:** ✅ DOWNLOADED

### williams_socioeconomic_race_comparison_2022.pdf
- **Source:** Williams Institute — "Race and Ethnicity of LGBT Adults in the United States"
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/LGBT-Race-Ethnicity-US-Sep-2022.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2022 | **Size:** 558KB
- **Coverage:** National; race/ethnicity breakdown of LGBT adults
- **Status:** ✅ DOWNLOADED

### williams_socioeconomic_black_lgbt_2021.pdf
- **Source:** Williams Institute — "Black LGBT Adults in the United States"
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/Black-LGBT-Adults-US-Jun-2021.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2021 | **Size:** 5.3MB
- **Coverage:** National; demographic, health, and economic profile of Black LGBT adults
- **Status:** ✅ DOWNLOADED

### williams_socioeconomic_education_college_2022.pdf
- **Source:** Williams Institute — "LGBT People and College Education"
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/LGBT-College-Education-Jan-2022.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2022 | **Size:** 4.1MB
- **Coverage:** National; education attainment comparison, student debt, major field
- **Status:** ✅ DOWNLOADED

### williams_socioeconomic_trans_nonbinary_lacounty_2024.pdf
- **Source:** Williams Institute — "Transgender and Nonbinary People in Los Angeles County"
- **URL:** `https://williamsinstitute.law.ucla.edu/wp-content/uploads/Trans-NB-LA-County-May-2024.pdf`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024 | **Size:** 4.9MB
- **Coverage:** Los Angeles County; detailed trans/nonbinary demographics and health
- **Caveats:** County-level deep-dive; use as model for other urban analyses
- **Status:** ✅ DOWNLOADED

**Additional socioeconomic sources needed:**
- `census_pums_2024_[1yr/5yr]_[person/household].csv` — Backbone of LGBTQ+ income/occupation/education analysis. Multi-GB files; local download required.
- `census_pums_occupation_codes_2024.xlsx` — `https://www.census.gov/topics/employment/industry-occupation/guidance/code-lists.html`
- `census_pums_industry_codes_2024.xlsx` — Same URL above
- `bls_oews_state_2024.zip` — See instructions in `economic/BLS_OEWS_DOWNLOAD_INSTRUCTIONS.txt`
- `map_family_formation_2025.csv` — MAP family data. `https://www.lgbtmap.org/equality-maps/parenting`
- `nhis_adult_2024.csv` — See Health section

---

## 9. GEOGRAPHIC REFERENCE DATA (`data/raw/geo/`)

### census_state_boundaries_500k.zip
- **Source:** U.S. Census Bureau — TIGER/Line Cartographic Boundary Files 2022
- **URL:** `https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_500k.zip`
- **Downloaded:** 2026-04-27 | **Size:** 3.0MB | Scale: 1:500,000
- **Coverage:** All 50 states + DC + territories | **Format:** ZIP → Shapefile (.shp, .dbf, .prj, .shx)
- **Status:** ✅ DOWNLOADED

### census_state_boundaries_5m.zip
- **Source:** U.S. Census Bureau — TIGER/Line 2022
- **URL:** `https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_5m.zip`
- **Downloaded:** 2026-04-27 | **Size:** 1.0MB | Scale: 1:5,000,000 (lighter weight for web maps)
- **Status:** ✅ DOWNLOADED

### census_county_boundaries_500k.zip
- **Source:** U.S. Census Bureau — TIGER/Line 2022
- **URL:** `https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_500k.zip`
- **Downloaded:** 2026-04-27 | **Size:** 11.1MB | Scale: 1:500,000
- **Coverage:** All ~3,200 U.S. counties
- **Status:** ✅ DOWNLOADED

### census_cbsa_boundaries_500k.zip
- **Source:** U.S. Census Bureau — TIGER/Line 2024 (2022 vintage was unavailable)
- **URL:** `https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_cbsa_500k.zip`
- **Downloaded:** 2026-04-27 | **Vintage:** 2024 | **Size:** 4.4MB | Scale: 1:500,000
- **Coverage:** Core Based Statistical Areas (metro + micro areas)
- **Status:** ✅ DOWNLOADED

### census_fips_state.txt
- **Source:** U.S. Census Bureau
- **URL:** `https://www2.census.gov/geo/docs/reference/codes2020/national_state2020.txt`
- **Downloaded:** 2026-04-27 | **Format:** Pipe-delimited
- **Coverage:** State FIPS codes for all 50 states + DC + territories
- **Status:** ✅ DOWNLOADED

### census_fips_county.txt
- **Source:** U.S. Census Bureau
- **URL:** `https://www2.census.gov/geo/docs/reference/codes2020/national_county2020.txt`
- **Downloaded:** 2026-04-27 | **Format:** Pipe-delimited | **Size:** 123KB
- **Coverage:** County FIPS codes for all U.S. counties
- **Status:** ✅ DOWNLOADED

---

## REMAINING DOWNLOADS CHECKLIST

Items still needed, in priority order:

| Priority | File | Source | Method | Notes |
|----------|------|---------|--------|-------|
| 1 | `census_pums_2024_1yr_person.csv` | Census.gov | Local download (~3GB) | Core LGBTQ+ microdata |
| 2 | `census_pums_2024_5yr_person.csv` | Census.gov | Local download (~15GB) | Core LGBTQ+ microdata |
| 3 | `census_pums_2024_*_household.csv` | Census.gov | Local download | Household-level analysis |
| 4 | `fbi_hatecrimes_all_2024.csv` | cde.ucr.cjis.gov | Browser download | Replace placeholder |
| 5 | `map_state_policy_scorecard_2025.csv` | lgbtmap.org | Manual compile | 50-state policy scores |
| 6 | `cdc_hiv_atlas_*.csv` | CDC NCHHSTP Atlas | Browser download | HIV by transmission |
| 7 | `nhis_adult_2024.csv` | CDC NCHS | Direct download | SOGI health indicators |
| 8 | `bls_oews_state_2024.zip` | bls.gov | Local browser download | IP-blocked from cloud |
| 9 | `census_pums_occupation_codes_2024.xlsx` | Census.gov | Direct download | PUMS crosswalk |
| 10 | `ncavp_hateviolence_2024.pdf` | avp.org | Direct PDF | Hate violence data |
| 11 | `glsen_state_snapshot_[state]_2024.pdf` | maps.glsen.org | 50 downloads | School climate by state |
| 12 | `aclu_legislation_tracker_2025.csv` | aclu.org | Manual compile | Anti-LGBTQ bills |
| 13 | `victory_fund_officials_2025.csv` | victoryfund.org | Manual compile | LGBTQ+ elected officials |
| 14 | `pride_events_compiled_2025.csv` | Wikipedia/InterPride | Manual compile | Event geography |
| 15 | `gss_crosssection_2024.csv` | gss.norc.org | Registration + download | Social attitudes |
| 16 | `hud_lgbtq_housing_[year].csv` | huduser.gov | Direct download | Housing discrimination |
| 17 | `irs_lgbtq_nonprofits_2026.csv` (full) | NCCS S3 | Local download (1.7GB) | Re-run for complete data |

---

*MANIFEST last updated: 2026-04-27. Run `find data/raw -type f | sort` to verify file presence.*
