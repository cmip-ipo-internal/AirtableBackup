'''
A script to backup the entire workspace in Airtable. 
This was designed for use by the IPO. 

Author and Maintainer - contact: 
Daniel Ellis (@wolfiex)
CMIP IPO Technical Officer. 
daniel.ellis (at) ext.esa.int

All copies of this program shall retain the original header statements as provided above. 
Additional features may be pushed on github, and the authors name and changes appended below. 
'''

import requests
import tqdm
import os
import pandas as pd
import concurrent.futures
import re
import json

# Airtable API endpoints
bases = 'https://api.airtable.com/v0/meta/bases'
schema = "https://api.airtable.com/v0/meta/bases/%(id)s/tables"
views = "https://api.airtable.com/v0/meta/bases/%(id)s/views"
records = "https://api.airtable.com/v0/%(baseId)s/%(tableIdOrName)s"


def clean_file_path_string(input_string: str) -> str:
    """
    Clean a string to make it suitable for file paths.

    Args:
        input_string (str): The input string to be cleaned.

    Returns:
        str: The cleaned string.
    """
    pattern = r'[<>:"/\\|?*\x00-\x1F\x7F-\x9F\s/]'
    cleaned_string = re.sub(pattern, '_', input_string)
    return cleaned_string


def mkdir(directory_path: str):
    """
    Create a directory if it doesn't exist.

    Args:
        directory_path (str): The path of the directory to create.
    """
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)


def jwrite(jsondata, location):
    """
    Write JSON data to a file.

    Args:
        jsondata: The JSON data to be written.
        location (str): The location (path) of the file to write to.
    """
    with open(location, 'w') as f:
        json.dump(jsondata, f, indent=4)


def entry(info, opt=''):
    """
    Create an entry dictionary.

    Args:
        info (dict): Information for the entry.
        opt (str): Additional options for the entry.

    Returns:
        dict: The entry dictionary.
    """
    return {'name': info.get('name'), 'id': info.get('id', ''), 'description': info.get('description', ''), 'children': [],
            'opt': opt}


def attach_table(csv_data, location, table_name):
    """
    Attach tables.

    Args:
        csv_data: The CSV data containing attachment information.
        location (str): The location (path) to save attachments.
        table_name (str): The name of the table.
    """

    pattern = r"'id': '([^']+)',\s*'url': '([^']+)',\s*'filename': '([^']+)',\s*'size': (\d+),\s*'type': '([^']+)'"
    ids = []
    urls = []
    filenames = []
    sizes = []
    filetypes = []
    matches = re.findall(pattern, csv_data)

    for match in matches:
        id, url, filename, size, filetype = match
        ids.append(id)
        urls.append(url)
        filenames.append(filename)
        sizes.append(int(size))
        filetypes.append(filetype)

    df = pd.DataFrame({'ID': ids, 'URL': urls, 'Filename': filenames, 'Size': sizes, 'Filetype': filetypes})

    if not matches:
        return False

    aloc = f'{location}/{table_name}_ATTACHMENTS'
    if not os.path.exists(aloc):
        os.mkdir(aloc)

    def download_file(args):
        row, aloc = args
        url = row['URL']
        filename = row['Filename']
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(f'{aloc}/{filename}', 'wb') as file, tqdm.tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                bar.update(len(data))
                file.write(data)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(download_file, [row, aloc]) for _, row in df.iterrows()]

    concurrent.futures.wait(futures)


def contents(base_path, schema):
    """
    Write contents to a file.

    Args:
        base_path (str): The base path where the contents file will be created.
        schema: The schema data to write as contents.
    """
    def print_hierarchy(node, f, indent=""):
        f.write(indent + f"{node['name']} ({node['id']})\n")
        if "children" in node:
            for child in node["children"]:
                print_hierarchy(child, f, indent + '\t')

    with open(f"{base_path}/contents.txt", 'w') as f:
        print_hierarchy(schema, f)


def dir_size(path: str, human_readable: bool = True):
    """
    Calculate the size of a directory in bytes or as a human-readable string.

    Args:
        path (str): The path to the directory to calculate the size for.
        human_readable (bool, optional): Whether to return the size as a human-readable string.
            Defaults to True.

    Returns:
        Union[int, str]: The size of the directory in bytes or as a human-readable string.
    """
    # Initialize size in bytes
    total_size = 0

    # Walk through all the files and subdirectories in the given directory
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Get the size of the file and add it to the total size
            total_size += os.path.getsize(filepath)

    if human_readable:
        # Define units for conversion
        units = ['bytes', 'KB', 'MB', 'GB', 'TB']

        # Find the appropriate unit and calculate the size in that unit
        unit_index = 0
        while total_size >= 1024 and unit_index < len(units) - 1:
            total_size /= 1024.0
            unit_index += 1

        # Format the size with two decimal places
        formatted_size = "{:.2f}".format(total_size)

        # Combine the size and unit for a user-friendly representation
        size_with_unit = f"{formatted_size} {units[unit_index]}"
        return size_with_unit
    else:
        return total_size
