# LGBTQ+ Atlas — Master Source Registry

**Generated:** 2026-04-27  
**Purpose:** Master registry of every organization and dataset used in the LGBTQ+ Atlas. This document will be used to generate the Atlas's public methodology page.

---

## 1. U.S. Census Bureau

| Field | Value |
|-------|-------|
| **Organization** | U.S. Census Bureau, U.S. Department of Commerce |
| **Primary URL** | https://www.census.gov |
| **Data Portal** | https://data.census.gov |
| **API Base** | https://api.census.gov/data/ |
| **PUMS Downloads** | https://www2.census.gov/programs-surveys/acs/data/pums/ |
| **Boundary Files** | https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html |
| **FIPS Codes** | https://www.census.gov/library/reference/code-lists/ansi.html |
| **License** | U.S. Government Work — public domain |
| **Terms of Use** | https://www.census.gov/data/developers/about/terms-of-service.html |
| **Citation** | U.S. Census Bureau, American Community Survey [year]-Year Estimates. Retrieved from Census Data API, [date]. |
| **Contact** | https://www.census.gov/about/contact-us.html |
| **Datasets used** | ACS 5-Year Tables: B11009, B11001, B12001, B15002, B15003, S1101, S1501; ACS 1-Year: B11009; PUMS 1-Year and 5-Year (person + household); Geographic Boundary Files (state, county, CBSA); FIPS Reference Tables |
| **Update cadence** | ACS 5-Year: December annually; ACS 1-Year: September annually; PUMS: same as ACS |

---

## 2. Williams Institute, UCLA School of Law

| Field | Value |
|-------|-------|
| **Organization** | Williams Institute at UCLA School of Law |
| **Primary URL** | https://williamsinstitute.law.ucla.edu |
| **Research Library** | https://williamsinstitute.law.ucla.edu/research/ |
| **Population Tool** | https://williamsinstitute.law.ucla.edu/visualization/lgbt-stats/ |
| **License** | Free for non-commercial use with attribution; see individual report licenses |
| **Terms of Use** | https://williamsinstitute.law.ucla.edu/terms/ |
| **Citation** | [Author(s)], "[Report Title]," Williams Institute, UCLA School of Law, [Month Year]. Available at [URL]. |
| **Contact** | info@williamsinstitute.law.ucla.edu |
| **Datasets used** | LGBT Adult Population Estimates (state-level, Dec 2023); Economic reports (poverty, income, workers); Socioeconomic profile reports (marriage, education, occupation); Family formation data |
| **Update cadence** | Reports published continuously; population estimates ~annual |

---

## 3. Movement Advancement Project (MAP)

| Field | Value |
|-------|-------|
| **Organization** | Movement Advancement Project |
| **Primary URL** | https://www.lgbtmap.org |
| **Equality Maps** | https://www.lgbtmap.org/equality-maps |
| **Family Formation** | https://www.lgbtmap.org/equality-maps/marriage and /parenting |
| **License** | Free for non-commercial use with attribution |
| **Terms of Use** | https://www.lgbtmap.org/about/terms |
| **Citation** | Movement Advancement Project, "Equality Maps," [year]. Available at https://www.lgbtmap.org/equality-maps. |
| **Contact** | info@lgbtmap.org |
| **Datasets used** | State Policy Scorecard (40+ policy categories, 50 states); Family Formation data (same-sex parenting, adoption policies) |
| **Update cadence** | Continuous (real-time updates to legislation); annual summary reports |
| **Notes** | No bulk CSV/API export. Data available through interactive maps and state profile pages. Manual compilation required. |

---

## 4. Human Rights Campaign (HRC)

| Field | Value |
|-------|-------|
| **Organization** | Human Rights Campaign |
| **Primary URL** | https://www.hrc.org |
| **MEI Page** | https://www.hrc.org/resources/municipal-equality-index |
| **2025 MEI Report** | https://reports.hrc.org/municipal-equality-index-2025 |
| **2024 MEI Report** | https://reports.hrc.org/municipal-equality-index-2024 |
| **License** | Free for non-commercial use with attribution |
| **Citation** | Human Rights Campaign Foundation, "Municipal Equality Index [Year]," Washington D.C.: HRC Foundation, [year]. Available at https://www.hrc.org/resources/municipal-equality-index. |
| **Contact** | mei@hrc.org (for data requests) |
| **Datasets used** | Municipal Equality Index 2025 (506 cities); MEI 2024 (for year-over-year) |
| **Update cadence** | Annual |
| **Notes** | PDF report freely available; structured CSV/Excel requires contacting HRC directly. |

---

## 5. Trans Legislation Tracker

| Field | Value |
|-------|-------|
| **Organization** | Trans Legislation Tracker (independent project) |
| **Primary URL** | https://translegislation.com |
| **Also at** | https://www.tracktranslegislation.com |
| **License** | Data freely accessible; no explicit license stated |
| **Citation** | Trans Legislation Tracker, "2025 Anti-Trans Bills," Available at https://translegislation.com/bills/2025. Retrieved [date]. |
| **Datasets used** | 2025 state-level bill counts (49 states, 1,022 bills); category breakdown; 2023–2025 national trend |
| **Update cadence** | Continuous during legislative sessions |
| **Notes** | No official bulk CSV export. State totals and categories extracted from embedded Next.js JSON. For individual bill details, see site directly or search for linked GitHub repositories. Uses LegiScan API for legislative data. |

---

## 6. ACLU

| Field | Value |
|-------|-------|
| **Organization** | American Civil Liberties Union |
| **Primary URL** | https://www.aclu.org |
| **Legislation Tracker** | https://www.aclu.org/legislative-attacks-on-lgbtq-rights |
| **License** | Free for non-commercial use |
| **Citation** | ACLU, "Legislative Attacks on LGBTQ+ Rights [year]," Available at https://www.aclu.org/legislative-attacks-on-lgbtq-rights. Retrieved [date]. |
| **Datasets used** | Anti-LGBTQ+ legislation tracker (bills by state, category, status) |
| **Update cadence** | Continuous |
| **Notes** | Interactive web tool; requires manual compilation to CSV. |

---

## 7. LGBTQ+ Victory Fund

| Field | Value |
|-------|-------|
| **Organization** | LGBTQ+ Victory Fund |
| **Primary URL** | https://victoryfund.org |
| **Candidates Page** | https://victoryfund.org/our-candidates/ |
| **License** | Free for non-commercial use with attribution |
| **Citation** | LGBTQ+ Victory Fund, "Out for America," Available at https://victoryfund.org/our-candidates/. Retrieved [date]. |
| **Datasets used** | Count of openly LGBTQ+ elected officials by state and level of office |
| **Update cadence** | Continuous |

---

## 8. Federal Bureau of Investigation (FBI)

| Field | Value |
|-------|-------|
| **Organization** | FBI Criminal Justice Information Services Division |
| **Primary URL** | https://www.fbi.gov |
| **Crime Data Explorer** | https://cde.ucr.cjis.gov |
| **API** | https://api.usa.gov/crime/fbi/sapi (requires api.data.gov key) |
| **API signup** | https://api.data.gov/signup/ |
| **License** | U.S. Government Work — public domain |
| **Citation** | FBI Crime Data Explorer, "Hate Crime Statistics [year]," U.S. Department of Justice. Available at https://cde.ucr.cjis.gov. |
| **Datasets used** | Hate crimes by state and agency, filtered by bias motivation: Sexual Orientation and Gender Identity; 2020–2024 |
| **Update cadence** | Annual (~12–16 months after reference year) |
| **Notes** | As of April 2026, 2024 data available. CDE requires browser interaction for bulk download. API key from api.data.gov enables programmatic access. Critical: document agencies NOT submitting data each year for underreporting adjustment. |

---

## 9. CDC — Behavioral Risk Factor Surveillance System (BRFSS)

| Field | Value |
|-------|-------|
| **Organization** | Centers for Disease Control and Prevention (CDC), NCCDPHP |
| **Primary URL** | https://www.cdc.gov/brfss/ |
| **Chronic Data Portal** | https://chronicdata.cdc.gov |
| **License** | U.S. Government Work — public domain |
| **Citation** | Centers for Disease Control and Prevention. Behavioral Risk Factor Surveillance System Survey Data. Atlanta, Georgia: U.S. Department of Health and Human Services, Centers for Disease Control and Prevention, [year]. |
| **Datasets used** | SOGI module: sexual orientation and gender identity variables; depression/mental health, healthcare avoidance, insurance coverage by SOGI status |
| **Update cadence** | Annual |
| **Notes** | Access via Socrata API at chronicdata.cdc.gov — search "BRFSS SOGI". Free, no registration required. |

---

## 10. CDC — National Center for HIV, Viral Hepatitis, STD, and TB Prevention (AtlasPlus)

| Field | Value |
|-------|-------|
| **Organization** | CDC NCHHSTP |
| **Atlas URL** | https://gis.cdc.gov/grasp/nchhstpatlas/main.html |
| **License** | U.S. Government Work — public domain |
| **Citation** | Centers for Disease Control and Prevention. AtlasPlus — HIV Surveillance Data, [year]. Available at https://gis.cdc.gov/grasp/nchhstpatlas/main.html. |
| **Datasets used** | HIV diagnoses by state and county; transmission category (male-to-male sexual contact); HIV care outcomes (linkage to care, viral suppression); 2020–2024 |
| **Update cadence** | Annual |
| **Notes** | Browser-based interactive tool; export via site interface. |

---

## 11. The Trevor Project

| Field | Value |
|-------|-------|
| **Organization** | The Trevor Project |
| **Primary URL** | https://www.thetrevorproject.org |
| **Research Page** | https://www.thetrevorproject.org/research-briefs/ |
| **2024 State Reports** | https://www.thetrevorproject.org/survey-2024-by-state/ |
| **License** | Free for non-commercial use with attribution |
| **Citation** | The Trevor Project. "2024 U.S. National Survey on the Mental Health of LGBTQ+ Young People." New York: The Trevor Project, February 2025. Available at https://www.thetrevorproject.org/survey-2024-by-state/. |
| **Datasets used** | 2024 national report (18,000+ LGBTQ+ youth ages 13–24); state-level reports for all 50 states + DC + PR; prior years 2020–2023 |
| **Update cadence** | Annual (published ~February each year) |
| **Key variables** | Suicidality rates, mental health support access, conversion therapy exposure, school safety, family acceptance — all by state and identity group |

---

## 12. GLSEN

| Field | Value |
|-------|-------|
| **Organization** | GLSEN (Gay, Lesbian and Straight Education Network) |
| **Primary URL** | https://www.glsen.org |
| **Survey Page** | https://www.glsen.org/research/national-school-climate-survey |
| **State Maps** | https://maps.glsen.org/state-research-snapshots/ |
| **License** | Free for non-commercial use with attribution |
| **Citation** | GLSEN. "2024 National School Climate Survey." New York: GLSEN, 2024. Available at https://www.glsen.org/research/2024-national-school-climate-survey. |
| **Datasets used** | 2024 National School Climate Survey (school year 2023–2024); state-level research snapshots |
| **Update cadence** | ~Every 2 years |
| **Key variables** | % students feeling unsafe at school; GSA club presence; anti-bullying policy coverage; LGBTQ-inclusive curriculum |

---

## 13. Gallup

| Field | Value |
|-------|-------|
| **Organization** | Gallup, Inc. |
| **Primary URL** | https://news.gallup.com/poll/lgbt.aspx |
| **2024 Report** | https://news.gallup.com/poll/656708/lgbtq-identification-rises.aspx |
| **License** | Free web access to published articles; raw data requires subscription |
| **Citation** | Jones, Jeffrey M. "LGBTQ+ Identification Rises to 9.3% in U.S." Gallup, February 2025. Available at https://news.gallup.com/poll/656708/lgbtq-identification-rises.aspx. |
| **Datasets used** | 2024 national LGBT identification (9.3% of U.S. adults); generational breakdown; identity type breakdown; historical trend 2012–2024 |
| **Update cadence** | Annual |
| **Notes** | Data compiled from published articles. State-level breakdowns available via Gallup subscription. ~14,162 adults surveyed in 2024. |

---

## 14. NCCS / Urban Institute

| Field | Value |
|-------|-------|
| **Organization** | National Center for Charitable Statistics (NCCS), Urban Institute |
| **Primary URL** | https://nccs.urban.org |
| **BMF Catalog** | https://nccs.urban.org/catalogs/catalog-bmf.html |
| **Latest BMF** | https://nccsdata.s3.us-east-1.amazonaws.com/processed/bmf/2026_01/bmf_2026_01_processed.csv |
| **License** | Public data; free for research use with attribution |
| **Citation** | Urban Institute, National Center for Charitable Statistics. Business Master File, January 2026. Available at https://nccs.urban.org/nccs/datasets/bmf/. |
| **Datasets used** | Business Master File (Jan 2026) filtered for LGBTQ+ organizations (NTEE P85 + keyword match) — ~5,000 orgs |
| **Update cadence** | Monthly |
| **Notes** | Full BMF is 1.7GB. Filtered extract contains ~4,981 rows (partial download — see MANIFEST). For complete dataset, download full BMF and filter for NTEE=P85 or name keywords: LGBT, LGBTQ, gay, lesbian, transgender, queer, bisexual, same-sex, pride. |

---

## 15. IRS / Tax Exempt Organizations (EOS)

| Field | Value |
|-------|-------|
| **Organization** | Internal Revenue Service |
| **Primary URL** | https://apps.irs.gov/app/eos/ |
| **License** | U.S. Government Work — public domain |
| **Citation** | IRS Tax Exempt Organization Search. Available at https://apps.irs.gov/app/eos/. Retrieved [date]. |
| **Datasets used** | Supplement to NCCS BMF for any gaps; NTEE code P85 lookup |
| **Notes** | Use NCCS/Urban Institute as primary source (cleaner, more structured). IRS EOS as backup for individual organization lookup. |

---

## 16. CDC — National Health Interview Survey (NHIS)

| Field | Value |
|-------|-------|
| **Organization** | CDC National Center for Health Statistics (NCHS) |
| **Primary URL** | https://www.cdc.gov/nchs/nhis/ |
| **Data Access** | https://www.cdc.gov/nchs/nhis/data-questionnaires-documentation.htm |
| **License** | U.S. Government Work — public domain |
| **Citation** | National Center for Health Statistics. National Health Interview Survey, [year]. Hyattsville, MD. 2026. |
| **Datasets used** | Adult Sample Person file with SOGI variables: sexual orientation (SEXORIEN_A), gender identity (GENDNBI_A), education, income, employment status, occupation |
| **Update cadence** | Annual (2024 data expected late 2025/early 2026) |
| **Key variables** | SRVY_YR, SEXORIEN_A, GENDNBI_A, EDUC_A, INCGRP_A, POVRATIO_A, EMPSTAT_A, OCCP_A, REGION |
| **Notes** | Federal government's own SOGI + economic data — valuable independent validation source. SOGI questions included since 2013. |

---

## 17. Bureau of Labor Statistics (BLS)

| Field | Value |
|-------|-------|
| **Organization** | U.S. Bureau of Labor Statistics |
| **Primary URL** | https://www.bls.gov/oes/ |
| **OES Tables** | https://www.bls.gov/oes/tables.htm |
| **License** | U.S. Government Work — public domain |
| **Citation** | U.S. Bureau of Labor Statistics, Occupational Employment and Wage Statistics, [year]. Available at https://www.bls.gov/oes/. |
| **Datasets used** | State-level OEWS data (oesm24st.zip) — reference table for translating PUMS occupation codes (OCCP) to occupation names and median wages |
| **Notes** | NOT LGBTQ+-specific. Required to decode PUMS microdata into readable occupation categories and attach wage benchmarks. |

---

## 18. General Social Survey (GSS)

| Field | Value |
|-------|-------|
| **Organization** | NORC at the University of Chicago |
| **Primary URL** | https://gss.norc.org |
| **Data Access** | https://gss.norc.org/get-the-data |
| **License** | Free for academic/non-commercial research with attribution |
| **Citation** | Smith, Tom W., Davern, Michael, Freese, Jeremy, and Morgan, Stephen, General Social Surveys, 1972-[year] [machine-readable data file]. Chicago: NORC, [year]. |
| **Datasets used** | Cross-sectional dataset with variables: sexornt, gender, marital, educ, degree, realinc, rincome, occ10, ind10, wrkstat, wrkslf, region, year |
| **Update cadence** | ~Every 2 years |
| **Notes** | Small sample sizes — do not use for state-level breakdowns. Useful for national trend analysis by sexual orientation from 2008–present. Registration may be required for download. |

---

## 19. HUD (Housing & Urban Development)

| Field | Value |
|-------|-------|
| **Organization** | U.S. Department of Housing and Urban Development |
| **Primary URL** | https://www.huduser.gov |
| **Dataset** | https://www.huduser.gov/portal/datasets/hsg_discrimination.html |
| **License** | U.S. Government Work — public domain |
| **Datasets used** | Housing discrimination testing data for same-sex couples; LGBTQ+ youth homelessness estimates by region |
| **Update cadence** | Periodic (study-based, not annual) |

---

## 20. InterPride

| Field | Value |
|-------|-------|
| **Organization** | InterPride — International Association of LGBTQ+ Pride Events |
| **Primary URL** | https://interpride.org |
| **Members List** | https://interpride.org/members |
| **License** | Free for non-commercial use |
| **Datasets used** | Pride event directory (city, country, member organization details) — for pride_events_compiled_2025.csv |
| **Notes** | Supplement with Wikipedia list of Pride parades and Eventbrite for attendance estimates. |

---

## DATA QUALITY & METHODOLOGICAL NOTES

### Same-Sex Couple Identification in Census PUMS
Since 2019, the Census Bureau directly asks about same-sex relationships in ACS. Prior years used a coding method that produced some misclassification. **Prefer 2019+ data** for same-sex couple analysis.

- **Married same-sex couples:** RELSHIPP=20 (spouse) + same SEX code + MAR=1
- **Cohabiting same-sex couples:** RELSHIPP=21 (unmarried partner) + same SEX code

### FBI Hate Crime Underreporting
Not all U.S. jurisdictions submit hate crime data to the FBI each year. The list of non-reporting agencies must be documented alongside reported counts to enable underreporting corrections. Check CDE for agency participation data.

### Data Vintage vs. Publication Year
Many datasets contain a data vintage year different from the publication year:
- ACS 2024 5-Year data (vintage 2020–2024) was published December 2025
- Trevor Project 2024 Survey (vintage 2024) was published February 2025
- FBI 2024 Hate Crimes (vintage 2024) published late 2025/early 2026
Always document both in MANIFEST.md.

### Williams Institute Methodology
Williams Institute estimates derive from Gallup Daily Tracking Survey and other national probability samples. State-level estimates use multilevel regression and poststratification (MRP). Sample sizes at state level can be small; treat estimates for low-population states with caution.
