## GWAS Summary Statistics Conversion Script

This script converts GWAS summary statistics (sumstats) data to the GWAS Summary Statistic Standard (GWAS-SSF) format for upload to the [IOmics mapOA](https://staging.iomics-mapoa.org/) website.

**Background:**

Association testing for all cohorts (except deCODE) in the GENOA GWAS meta-analyses used the score test model of rvtests.
This resulted in sumstats files with a relatively consistent format, except a few minor variations between cohorts. 

**Conversion to GWAS-SSF:**

The GWAS-SSF is a standardized format for GWAS summary statistics, promoting data sharing and analysis across studies.
Converting our sumstats to this format simplifies upload to IOmics mapOA.

**Why a Custom Script?**

While the [gwas-sumstats-tools](https://github.com/EBISPOT/gwas-sumstats-tools.git) offered a promising solution for conversion, we encountered limitations.
That is, in addition to the required fields for GWAS-SSF, we wanted to included the encouraged fields `rsid` and `variant_id`. 
In order to extract the information from our results to create these fields, it required some custom logic due to the complexity and variations in the ID fields of our sumstats (e.g., `rs544698705:672940:G:C`, `1:768116:A:AGTTTT`, `1:766600:<CN0>:G`,  `1:3011887:<INS:ME:ALU>:A`)

We explored using a configuration file for gwas-sumstats-tools, which offers powerful data manipulation capabilities.
However, the specific formatting needed for our `ID` column wasn't achievable through this method.

**Custom Script Functionality:**

Our custom script addresses these challenges by:

* Splitting the `ID` column based on regular expressions to capture `rsid`, variant information, and create the `variant_id` field as outlined in the [GWAS-SSF v1.0.0](https://github.com/EBISPOT/gwas-summary-statistics-standard/blob/master/gwas-ssf_v1.0.0.pdf) standard.
* Handling different variant ID formats encountered in the data.

**Benefits:**

This script facilitates:

* Consistent GWAS-SSF compliant data for upload to IOmics mapOA.
* Improved data sharing and analysis possibilities.
