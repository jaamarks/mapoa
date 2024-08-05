import typer
import os
import json
import pprint

from ckanapi import RemoteCKAN, ValidationError
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from mapoa_api_utils import yaml_to_json, check_dataset_required_fields


app = typer.Typer()

load_dotenv()  # This will load variables from the .env file

api_url = os.environ.get("MAPOA_API_URL")
api_key = os.environ.get("MAPOA_API_TOKEN")

if not api_url:
    raise ValueError("MAPOA_API_URL environment variable not set!")
if not api_key:
    raise ValueError("MAPOA_API_TOKEN environment variable not set!")

# Initializes and returns a RemoteCKAN client object with user credentials.
mapoa = RemoteCKAN(api_url, apikey=api_key)


@app.command()
def list_datasets(
    include_private: bool = True,
    detailed_output: Annotated[bool, typer.Argument(help="Print all metadata associated with the datasets, else just print the name.")] = False
    ):
    """
    Lists accessible datasets (public or private).
    """

    datasets = mapoa.call_action("package_search", {"include_private": include_private})

    if detailed_output:
        typer.echo(f"Datasets: {datasets}")
    else:
        for result in datasets["results"]:
            styled_name = typer.style(result["name"], fg=typer.colors.GREEN)
            typer.echo(styled_name)


@app.command()
def list_datasets_with_resources():
    """
    Lists all datasets along with their metadata and resources.
    """
    package_resources = mapoa.call_action("current_package_list_with_resources")
    typer.echo(f"Package Resources: {package_resources}")


@app.command()
def list_organizations():
    """
    Return a list of the names of the site’s organizations.
    """
    orgs = mapoa.action.organization_list()
    typer.echo(f"\nOrganizations: {orgs}\n")


@app.command()
def list_tags():
    """
    Lists all tags associated with at least one dataset on mapOA.
    """
    tags = mapoa.call_action("tag_list")
    typer.echo(f"Tags: {tags}")


@app.command()
def show_dataset(dataset_id: str):
    """
    Shows detailed metadata for a specific dataset identified by its ID.
    """
    dataset_metadata = mapoa.call_action("package_show", {"id": dataset_id})
    typer.echo(f"Dataset Metadata: {dataset_metadata}")


@app.command()
def search_datasets(query: str):
    """
    Searches for datasets based on the provided query string.
    """
    search_results = mapoa.call_action("package_search", {"q": query})
    typer.echo(f"Search Results: {search_results}")


@app.command()
def create_package(dataset: Annotated[Path, typer.Argument(help="JSON file containing required parameters. See `templates/template_package.json`.")]):
    """
    Create a new dataset (package).

    You must be authorized to create new datasets.
    If you specify any groups for the new dataset, you must also be authorized to edit these groups.
    Searches for datasets based on the provided query string.
    https://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.create.package_create
    """

    with open(dataset, 'r') as f:
        data_dict = json.load(f)

    dataset = check_dataset_required_fields(data_dict)
    if dataset is None:  # Check for None returned by inner function
        return  # Ex

    try:
        mapoa.call_action("package_create", dataset)
        pass
    except ValidationError as e:
        #typer.echo("ValidationError attributes and methods:")
        #typer.echo(dir(e))
        if 'name' in e.error_dict and 'That URL is already in use.' in e.error_dict['name']:
            typer.echo("This package name already exists.")
            return
        else:
            typer.echo(f"Validation error: {e}")
            return

    message = f"Success! Created package '{dataset["name"]}'\n"
    typer.echo(message)
    pprint.pprint(dataset)


@app.command()
def upload_resources(
    required_fields: Annotated[Path, typer.Argument(help="JSON file containing required parameters. See `templates/template_resources.json`.")],
    sumstats: Annotated[Path, typer.Argument(help="GWAS SSF sumstats file (TSV).")],
    metadata: Annotated[Path, typer.Argument(help="GWAS SSF metadata file (YAML).")]
    ):

    """
    Adds a GWAS-SSF resource to the datasets list.

    This function uploads a GWAS Summary Statistics Format (GWAS-SSF) file
    and its accompanying metadata (YAML) file.

    \n
    GWAS-SSF consists of two files:\n
    * Summary statistics data file (TSV): e.g., "0000123.tsv" containing the actual GWAS data.\n
    * Accompanying metadata file (YAML): e.g., "0000123.tsv-meta.yaml" providing additional information about the study.

    \n
    The 3rd required file is a JSON file for the required_fields parameter, which will be appended to the metadata (YAML). Note, you may also include additional fields in this JSON that are not present in the metadata file.

    \n
    Resources:\n
    * GWAS-SSF Standard: https://github.com/EBISPOT/gwas-summary-statistics-standard/tree/master\n
    * CKAN API Reference: https://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.create.resource_create
    """
    metadata_resource = yaml_to_json(metadata)

    with open(required_fields, 'r') as file1, open(sumstats, 'r') as file2, open(metadata, 'r') as file3:
        data_dict = json.load(file1)
        metadata_resource.update(data_dict)
        #print(metadata_resource)

        mapoa.call_action("resource_create", metadata_resource, files={"upload": file2})
        mapoa.call_action("resource_create", metadata_resource, files={"upload": file3})

        # same metadata for both uploads
        styled_sumstats = typer.style(sumstats, fg=typer.colors.GREEN)
        styled_metadata = typer.style(metadata, fg=typer.colors.GREEN)
        message = f"\nUploaded resources:\n- {styled_sumstats}\n- {styled_metadata}."
        typer.echo(message)


if __name__ == "__main__":
    app()
