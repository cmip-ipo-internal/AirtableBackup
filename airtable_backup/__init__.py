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
import os
import json
import time
import requests
import pandas as pd
from datetime import datetime
import tqdm
from .helpers import *
from .splash import hline

class AirtableBackup:
    def __init__(self):
        """
        Initialize the AirtableBackup instance.

        Attributes:
            current_date (str): The current date in YYMMDD format.
            BLOCATION (str): The location where backups will be stored.
            AIRTABLE_API_KEY (str): The Airtable API key.
            WRITE (bool): Flag indicating whether to write data to CSV files.
            ATTACHMENTS (bool): Flag indicating whether to handle attachments.
            headers (dict): HTTP headers for Airtable API requests.
        """
        self.current_date = datetime.now().strftime("%y%m%d")
        self.BLOCATION = os.environ.get('AIRTABLE_BACKUP')
        self.AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')

        hline()
        print(f' Backup Location: {self.BLOCATION}')
        assert self.AIRTABLE_API_KEY, "AIRTABLE_API_KEY environment variable is not set."
        assert os.path.exists(self.BLOCATION), "Backup location does not exist."

        self.WRITE = True
        self.ATTACHMENTS = True

        self.headers = {
            'Authorization': f'Bearer {self.AIRTABLE_API_KEY}',
        }

    def get(self, url: str) -> dict:
        """
        Send a generic HTTP GET request to the specified URL.

        Args:
            url (str): The URL to send the GET request to.

        Returns:
            dict: The JSON response from the GET request.

        Raises:
            AssertionError: If the response status code is not 200 after multiple retries.
        """
        counter = 10
        while counter:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            counter -= 1
            time.sleep(0.3)
        assert False, f"Error: {response.status_code}"

    def start(self):
        """
        Start the Airtable backup process.
        """
        start_time = time.time()
        # Initialize the master entry for the backup
        master = entry(dict(name='CMIP-IPO', description='Top level of all the bases.'))

        # Get information about all bases
        data_bases = self.get(bases)['bases']
        assert data_bases

        # Create a directory for the backup
        base_path = f'{os.path.abspath(self.BLOCATION)}/backup_{self.current_date}'
        mkdir(base_path)

        # Iterate through each base
        for base in tqdm.tqdm(data_bases):
            basedir = f"{base_path}/{base['name'].replace(' ', '_')}"
            mkdir(basedir)

            masterbase = entry(base, 'base')

            # Get schema information for the base and write it to a JSON file
            tables = self.get(schema % base)['tables']
            jwrite(tables, f"{basedir}/schema.json")

            print(f"Base ID: {base['id']}, Base Name: {base['name']}")

            # Iterate through tables in the base
            children = []
            for table in tables:
                dummy = entry(table, 'table')
                dummy['fields'] = [dict(type=i.get('type'), name=i.get('name'), id=i.get('id')) for i in
                                   table.get('fields', [])]
                views = []

                # Iterate through views in the table
                for v in table.get('views', []):
                    views.append(entry(v, 'views'))

                dummy['children'] = views
                children.append(dummy)

                # Write table data to a CSV file
                if self.WRITE:
                    tjs = [{"airid": i['id'], **i['fields']} for i in
                            self.get(records % dict(baseId=base['id'], tableIdOrName=table['id']))['records']]
                    tname = clean_file_path_string(table['name'])
                    csv_data = pd.read_json(json.dumps(tjs)).to_csv()

                    location = f"{basedir}/{tname}.csv"
                    with open(location, 'w') as f:
                        f.write(csv_data)

                    if self.ATTACHMENTS:
                        attach_table(csv_data, basedir, tname)

            masterbase['children'] = children

            master['children'].append(masterbase)

        # Write the master schema to a JSON file
        jwrite(master, f"{base_path}/plotschema.json")

        # Create a contents file for the backup
        contents(base_path, master)

        end_time = time.time()
        elapsed_time_seconds = end_time - start_time
        elapsed_time_minutes = elapsed_time_seconds / 60


        hline()
        print( ' CMIP - International Project Office Backup')
        hline()
        print('\n')
        hline('-')
        print(f' Backup Location         : {base_path}')
        print(f' Save Tables|Attachments : {self.WRITE} {self.WRITE & self.ATTACHMENTS}')
        # print(f' Number of Bases         : {len(data_bases)}')
        print(f' Total Elapsed Time (min): {elapsed_time_minutes}')
        print(f' Total Backup Size       : {dir_size(base_path)}')
        hline('-')
