from typing import Optional
import typer
from ckanapi import RemoteCKAN
import os
from dotenv import load_dotenv


app = typer.Typer()

load_dotenv()  # This will load variables from the .env file

api_url = os.environ.get("MAPOA_API_URL")
api_key = os.environ.get("MAPOA_API_TOKEN")

if not api_url:
    raise ValueError("MAPOA_API_URL environment variable not set!")
if not api_key:
    raise ValueError("MAPOA_API_TOKEN environment variable not set!")


def get_mapoa_client():
    """
    Initializes and returns a RemoteCKAN client object with user credentials.
    """
    return RemoteCKAN(api_url, apikey=api_key)

@app.command()
def list_datasets(include_private: bool = True):
    """
    Lists all datasets (public or private based on the flag)
    accessible to the user.
    """
    mapoa = get_mapoa_client()
    datasets = mapoa.call_action("package_search", {"include_private": include_private})
    typer.echo(f"Datasets: {datasets}")


@app.command()
def list_datasets_with_resources():
    """
    Lists all datasets along with their metadata and resources.
    """
    mapoa = get_mapoa_client()
    package_resources = mapoa.call_action("current_package_list_with_resources")
    typer.echo(f"Package Resources: {package_resources}")


@app.command()
def list_tags():
    """
    Lists all tags associated with at least one dataset on mapOA.
    """
    mapoa = get_mapoa_client()
    tags = mapoa.call_action("tag_list")
    typer.echo(f"Tags: {tags}")


@app.command()
def show_dataset(dataset_id: str):
    """
    Shows detailed metadata for a specific dataset identified by its ID.
    """
    mapoa = get_mapoa_client()
    dataset_metadata = mapoa.call_action("package_show", {"id": dataset_id})
    typer.echo(f"Dataset Metadata: {dataset_metadata}")


@app.command()
def search_datasets(query: str):
    """
    Searches for datasets based on the provided query string.
    """
    mapoa = get_mapoa_client()
    search_results = mapoa.call_action("package_search", {"q": query})
    typer.echo(f"Search Results: {search_results}")


if __name__ == "__main__":
    app()

