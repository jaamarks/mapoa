# mapOA CLI
This handy CLI enables you to easily interact with data on the [mapOA](https://staging.iomics-mapoa.org/) website.
We picked some of the most useful commands from the `ckanapi` Python module, which allows you to call anything listed in the [CKAN Action API](https://docs.ckan.org/en/latest/api/index.html#action-api-reference), and used [Typer](https://github.com/tiangolo/typer) to create a user-friendly interface. 
The goal was to simplify retrieving information—like datasets (AKA packages in CKAN)—from mapOA.

**Forked from:** `https://github.com/RTIInternational/mapMECFS-API/blob/main/python/mapMECFS-API.py`



<br><br>



## Installation
Install dependencies with conda:
```shell
conda env create -f environment.yaml
conda activate mapoa_cli  # Replace with your environment name
```

<br><br>


## Configuration
The CLI uses environment variables to store sensitive information like API credentials.
You'll need to edit the hidden file named `.env` that is in the same directory as the CLI.
Set the following variables:

* **`MAPOA_API_URL`:** The base URL of the mapOA API. By default, it points to the staging environment: `https://staging.iomics-mapoa.org/`. Update this value if you need to access a different environment.
* **`MAPOA_API_TOKEN`:** Your personal API token retrieved from your mapOA user profile page. This token grants access to the API and should be kept confidential.


**Example:**
```
MAPOA_API_URL=https://staging.iomics-mapoa.org/
MAPOA_API_TOKEN=MyEXampleAPIKeyI1NiJ9eyJqdGkiOiJwZ2ZGUEFTaEtaWnEXAMPLElKSUswMHJlbexamplemRLa1YtWWRvZmhkQVJQYVotT3FYT2owIiwiaWF0IjoxN4fQ.3HvcveO1vXhqUbKqkr76YVKdreXAMPL3
```

**Important:** Replace `MAPOA_API_KEY` with your actual API token.


<br><br>




## Usage
<p align="center"><img src="mapoa_api_demo.gif"/></p>

<br><br>

### Uploading GWAS Data

To upload GWAS data, follow these two steps:

**1. Create an Analysis:**

   * Use the `create-dataset` command with a dataset JSON file.
   * Create a copy of `templates/template_dataset.json` as a starting point.
   * Provide the following required information:
     * `title`: The display name of the dataset.
     * `name`: A unique identifier (lowercase alphanumeric, 2-100 characters).
     * `notes`: A description of the dataset.
     * `owner_org`: The ID of the dataset's owning organization (find using `list-organizations`).
     * `analysisType`: Either `primary` or `meta-analysis`.
     * `dataType`: The type of dataset.
     * `private`: Set to `true` for a private dataset, `false` for public (no quotes).

   **For more detailed information on the `create-dataset` command run:**

   ```bash
   python mapoa_api.py create-dataset --help
   ```

**2. Upload GWAS Data:**
   * Use the `upload-resources` command with a resources JSON file, SSF sumstats, and metadata files.
   * Create a copy of `templates/template_resources.json` as a starting point.
   * Replace the `package_id` in the JSON with the `name` of the analysis created in step 1.

   **Important:** The order of arguments you supply to the `upload-resources` command matters. Use the following command for more detailed information on the expected order and available options.

   ```
   python mapoa_api.py upload-resources --help
   ```

**Note:** CKAN uses the terms "dataset" and "package" interchangeably. For MapOA, we refer to this as an "Analysis."