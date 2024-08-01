from typing import Optional
import typer
from ckanapi import RemoteCKAN
import os
from dotenv import load_dotenv
from pathlib import Path


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

#def get_mapoa_client():
#    """
#    """
#    return RemoteCKAN(api_url, apikey=api_key)

@app.command()
def list_datasets(include_private: bool = True):
    """
    Lists all datasets (public or private based on the flag)
    accessible to the user.
    """
    datasets = mapoa.call_action("package_search", {"include_private": include_private})
    typer.echo(f"Datasets: {datasets}")


@app.command()
def list_datasets_with_resources():
    """
    Lists all datasets along with their metadata and resources.
    """
    package_resources = mapoa.call_action("current_package_list_with_resources")
    typer.echo(f"Package Resources: {package_resources}")


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
def create_package(package_name: str):
    """
    Create a new dataset (package).

    You must be authorized to create new datasets.
    If you specify any groups for the new dataset, you must also be authorized to edit these groups.
    Searches for datasets based on the provided query string.
    https://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.create.package_create
    """
    dataset = {
        "name": package_name,
        "notes" : f"API Test: {package_name}",
        "data_type": "GWAS",
        "owner_org": "jaamarks-org",
        "maintainer": "Jesse Marks",
        "maintainer_email": "jmarks@rti.org",
    }

    mapoa.call_action("package_create", dataset)
    print(f"Success! Created a package: {package_name}")


@app.command()
def upload_resources(sumstats: Path, metadata: Path):
    """
    Adds a new GWAS resource to the datasets list.

    This function uploads a GWAS Summary Statistics Format (GWAS-SSF) file
    and its accompanying metadata (YAML) file.\n
    GWAS-SSF consists of two files:\n
    * Summary statistics data file (TSV): e.g., "0000123.tsv" containing
      the actual GWAS data.\n
    * Accompanying metadata file (YAML): e.g., "0000123.tsv-meta.yaml"
      providing additional information about the study.

    \n
    Resources:\n
    * GWAS-SSF Standard: https://github.com/EBISPOT/gwas-summary-statistics-standard/tree/master\n
    * CKAN API Reference: https://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.create.resource_create
    """


if __name__ == "__main__":
    app()

