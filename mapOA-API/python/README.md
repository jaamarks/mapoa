# mapOA CLI
This Python CLI allows you to interact with the mapOA data API.
You can use it to retrieve or list datasets from the [mapOA](https://staging.iomics-mapoa.org/) website.
CKAN documentation of the API in a general context is available at `https://github.com/ckan/ckanapi`

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