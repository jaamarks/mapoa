## GWAS Summary Statistics Conversion Script

This script converts GWAS summary statistics (sumstats) data to the GWAS Summary Statistic Standard (GWAS-SSF) format for upload to the [IOmics mapOA](https://staging.iomics-mapoa.org/) website.

<br>

**Background:**

In the GENOA GWAS meta-analyses, all cohorts (excluding deCODE) used the score test model from rvtests ([PMID36207451](https://pubmed.ncbi.nlm.nih.gov/36207451/)) for association testing.
This resulted in sumstats files with a generally consistent format, with minor variations between cohorts. 

**Importance of GWAS-SSF Conversion:**

The [GWAS-SSF](https://www.ebi.ac.uk/gwas/docs/methods/summary-statistics) is a standardized format for GWAS summary statistics, promoting data sharing and analysis across studies.
Converting our sumstats to this format simplifies upload to the IOmics mapOA platform.

**Why a Custom Script?**

While the [gwas-sumstats-tools](https://github.com/EBISPOT/gwas-sumstats-tools.git) offered a potential conversion solution, limitations arose.
That is, in addition to the required fields for GWAS-SSF, we wanted to included the encouraged fields `rsid` and `variant_id`. 
In order to extract the information from our results to create these fields, it required some custom logic due to the complexity and variations in the ID fields of our sumstats (e.g., `rs544698705:672940:G:C`, `1:768116:A:AGTTTT`, `1:766600:<CN0>:G`,  `1:3011887:<INS:ME:ALU>:A`)

Although gwas-sumstats-tools allows powerful data maniputation through configuration files, the specific formatting needed for our `ID` column exceeded its capabilities.

**Custom Script Functionality:**

Our custom script addresses these challenges by:

* Splitting the `ID` column based on regular expressions to capture `rsid`, variant information, and create the `variant_id` field as outlined in the [GWAS-SSF v1.0.0](https://github.com/EBISPOT/gwas-summary-statistics-standard/blob/master/gwas-ssf_v1.0.0.pdf) standard.
* Effectively handling disparate variant ID formats present in the data.

**Benefits of Using This Script:**

* Ensures consistent GWAS-SSF compliance for uploading data to IOmics mapOA.
* Enhances data sharing and analysis opportunities.
