import typer
import json, yaml

from pathlib import Path


def _remove_section_headers(yaml_dict: dict):
    """
    Removes section headers from a YAML dictionary to create a flat structure.

    This function is necessary for extracting data for the Additional Information table
    on the mapOA website, which requires a flat YAML structure.

    Args:
        yaml_dict (dict): The input YAML dictionary with potential section headers.

    Returns:
        dict: A new dictionary with section headers removed, resulting in a flat structure.
    """

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


# annotate that it returns a dict
def yaml_to_json(yaml_file: Path):
  """Converts a YAML file to a dict.

  Args:
    yaml_file: The path to the YAML file.
  """

  with open(yaml_file, 'r') as yaml_stream:
    data = yaml.load(yaml_stream,  Loader=yaml.BaseLoader)
    data = _remove_section_headers(data)
    for key, value in data.items():
        if isinstance(value, list):
            data[key] = f"[{', '.join(map(str, value))}]"
    return data


def check_dataset_required_fields(data):
    required_fields = ["name", "maintainer", "maintainer_email"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        print(f"Missing required fields: {', '.join(missing_fields)}")
        return None
    else:
        return data