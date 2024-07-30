import yaml
import json
from ckanapi import RemoteCKAN
from werkzeug.datastructures import FileStorage
import json, yaml
from base64 import b64encode
import os
from dotenv import load_dotenv


def main(file_path):
    load_dotenv()  # This will load variables from the .env file

    api_url = os.environ.get("MAPOA_API_URL")
    api_key = os.environ.get("MAPOA_API_TOKEN")

    mapoa = RemoteCKAN(api_url, apikey = api_key)

    resource_test = yaml_to_json(gwas_metadata_path)

    with open(file_path, 'rb') as file1:
        mapoa.call_action("resource_create", resource_test, files={"upload": file1})
    print(f"Created resource: {resource_test}.")


def update_json(data):
    data.update({
        "title": "API Test",
        "package_id": "api-test3",
        "name": "Test GWAS UHS123 Chr6",
        "description": "Resource for API Test3 dataset",
        "analysisType": "primary",
        "resource_file_type": "Results File", # expected values include: Data File, Phenotype File, Results File, and Supporting File
    })
    return data


def remove_section_headers(yaml_dict):
    new_dict = {}
    for key, value in yaml_dict.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    new_dict.update(item)
                else:
                    new_dict[key] = value
        else:
            new_dict[key] = value
    return new_dict


def yaml_to_json(yaml_file):
  """Converts a YAML file to a dict.

  Args:
    yaml_file: The path to the YAML file.
  """

  with open(yaml_file, 'r') as yaml_stream:
    data = yaml.load(yaml_stream,  Loader=yaml.BaseLoader)
    data = remove_section_headers(data)
    for key, value in data.items():
        if isinstance(value, list):
            data[key] = f"[{', '.join(map(str, value))}]"
    data = update_json(data)
    #print(json.dumps(data, indent=4))
    return data

if __name__ == "__main__":
    gwas_metadata_path = "/Users/jmarks/Library/CloudStorage/OneDrive-ResearchTriangleInstitute/Projects/p50/mapoa/github/jaamarks/mapoa/mapOA-API/python/uhs1-2-3.aa.oaall.genome_wide.gwas_ssf.tsv-meta.yaml.txt"
    main(gwas_metadata_path)
